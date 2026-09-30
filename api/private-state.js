const crypto = require("crypto");

function safeEqual(a, b) {
  const left = Buffer.from(String(a || ""));
  const right = Buffer.from(String(b || ""));
  if (left.length !== right.length) return false;
  return crypto.timingSafeEqual(left, right);
}

function authorized(req) {
  const configured = process.env.CONTROL_CENTER_BEARER;
  if (!configured) return { ok: false, reason: "not_configured" };

  const auth = req.headers.authorization || "";
  const bearer = auth.startsWith("Bearer ") ? auth.slice(7) : "";
  const alternate = req.headers["x-command-center-token"] || "";
  const provided = bearer || alternate;

  return { ok: safeEqual(provided, configured), reason: "invalid_token" };
}

async function github(path) {
  if (!process.env.GITHUB_TOKEN) {
    throw new Error("github_private_token_unconfigured");
  }
  const response = await fetch(`https://api.github.com${path}`, {
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      "User-Agent": "stein-agent-factory-private-control"
    }
  });
  if (!response.ok) throw new Error(`github_${response.status}`);
  return response.json();
}

async function googleAccessToken() {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const refreshToken = process.env.GOOGLE_REFRESH_TOKEN;

  if (!clientId || !clientSecret || !refreshToken) return null;

  const body = new URLSearchParams({
    client_id: clientId,
    client_secret: clientSecret,
    refresh_token: refreshToken,
    grant_type: "refresh_token"
  });

  const response = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body
  });

  if (!response.ok) throw new Error(`google_oauth_${response.status}`);
  const payload = await response.json();
  return payload.access_token;
}

async function driveIndex() {
  const q = process.env.DRIVE_Q;
  if (!q) return { status: "UNCONFIGURED", reason: "DRIVE_Q missing" };

  const token = await googleAccessToken();
  if (!token) {
    return { status: "UNCONFIGURED", reason: "Google OAuth env missing" };
  }

  const params = new URLSearchParams({
    q,
    pageSize: "100",
    orderBy: "modifiedTime desc",
    fields: "files(id,name,mimeType,modifiedTime,webViewLink,parents)"
  });

  const response = await fetch(`https://www.googleapis.com/drive/v3/files?${params}`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!response.ok) throw new Error(`drive_${response.status}`);
  const payload = await response.json();

  return {
    status: "LIVE",
    files: (payload.files || []).map((file) => ({
      id: file.id,
      name: file.name,
      mimeType: file.mimeType,
      modifiedTime: file.modifiedTime,
      webViewLink: file.webViewLink,
      parents: file.parents || []
    }))
  };
}

async function repoSnapshot(repo) {
  const [metadata, issues, pulls, main] = await Promise.all([
    github(`/repos/${repo}`),
    github(`/repos/${repo}/issues?state=open&per_page=100`),
    github(`/repos/${repo}/pulls?state=open&per_page=100`),
    github(`/repos/${repo}/commits/main`)
  ]);

  return {
    repo,
    visibility: metadata.visibility,
    pushedAt: metadata.pushed_at,
    mainSha: main.sha,
    issues: issues
      .filter((item) => !item.pull_request)
      .map((item) => ({
        number: item.number,
        title: item.title,
        state: item.state,
        updatedAt: item.updated_at,
        url: item.html_url
      })),
    pullRequests: pulls.map((item) => ({
      number: item.number,
      title: item.title,
      state: item.state,
      draft: item.draft,
      updatedAt: item.updated_at,
      url: item.html_url,
      headSha: item.head && item.head.sha
    }))
  };
}

module.exports = async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "method_not_allowed" });
  }

  res.setHeader("Cache-Control", "no-store");

  const auth = authorized(req);
  if (!auth.ok) {
    return res.status(auth.reason === "not_configured" ? 503 : 401).json({
      error: auth.reason,
      privateState: "LOCKED"
    });
  }

  const repos = (process.env.CONTROL_PRIVATE_REPOS ||
    "denistein2/ERPFoodControl,denistein2/Stein-Brain")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);

  const output = {
    version: "private-control-state-v1",
    generatedAt: new Date().toISOString(),
    exposure: "PRIVATE_AUTHENTICATED",
    sources: {
      github: { status: "UNCONFIGURED", repositories: [] },
      drive: { status: "UNCONFIGURED" }
    },
    focus: {
      repo: "denistein2/ERPFoodControl",
      orderedIssueNumbers: [66, 58, 50, 57, 56, 63, 49],
      fiscalTrack: "Issue #48 Track B",
      purchasesTrack: "Issue #48 Track D",
      productionStockExpansion: "DEFERRED"
    }
  };

  try {
    const repositories = [];
    for (const repo of repos) {
      repositories.push(await repoSnapshot(repo));
    }
    output.sources.github = { status: "LIVE", repositories };

    const erp = repositories.find((item) => item.repo === "denistein2/ERPFoodControl");
    if (erp) {
      const byNumber = new Map(erp.issues.map((issue) => [issue.number, issue]));
      output.focus.queue = output.focus.orderedIssueNumbers
        .map((number, index) => {
          const issue = byNumber.get(number);
          return issue
            ? { order: index + 1, ...issue }
            : { order: index + 1, number, state: "NOT_FOUND_OR_CLOSED" };
        });
    }

    const brain = repositories.find((item) => item.repo.toLowerCase().includes("stein-brain"));
    if (brain) {
      output.sources.brain = {
        status: "LIVE",
        repo: brain.repo,
        mainSha: brain.mainSha,
        pushedAt: brain.pushedAt,
        openIssues: brain.issues.length,
        openPullRequests: brain.pullRequests.length
      };
    }
  } catch (error) {
    output.sources.github = { status: "DEGRADED", error: error.message, repositories: [] };
  }

  try {
    output.sources.drive = await driveIndex();
  } catch (error) {
    output.sources.drive = { status: "DEGRADED", error: error.message };
  }

  output.submarine = {
    mode: "OFF",
    writeAuthority: false,
    auditGateIssue: 17,
    controlPlaneIssue: 20,
    note: "Read-only telemetry only. No autonomous write path is enabled."
  };

  output.auditor = {
    claudeCode: {
      status: "PLANNED_NOT_CONNECTED",
      role: "independent adversarial red team / code audit"
    }
  };

  return res.status(200).json(output);
};
