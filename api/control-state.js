const REPO = "denistein2/AgentFactory";

async function github(path) {
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": "stein-agent-factory-command-center"
  };
  if (process.env.PUBLIC_GITHUB_TOKEN) {
    headers.Authorization = `Bearer ${process.env.PUBLIC_GITHUB_TOKEN}`;
  }

  const response = await fetch(`https://api.github.com${path}`, { headers });
  if (!response.ok) {
    const error = new Error(`GitHub ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return response.json();
}

module.exports = async function handler(req, res) {
  if (req.method !== "GET") {
    res.setHeader("Allow", "GET");
    return res.status(405).json({ error: "method_not_allowed" });
  }

  res.setHeader("Cache-Control", "public, s-maxage=30, stale-while-revalidate=120");

  const generatedAt = new Date().toISOString();
  let githubState = {
    status: "DEGRADED",
    repo: REPO,
    openIssues: null,
    openPullRequests: null,
    mainSha: null,
    tracked: []
  };

  try {
    const [repository, issues, pulls, main] = await Promise.all([
      github(`/repos/${REPO}`),
      github(`/repos/${REPO}/issues?state=open&per_page=100`),
      github(`/repos/${REPO}/pulls?state=open&per_page=100`),
      github(`/repos/${REPO}/commits/main`)
    ]);

    const realIssues = issues.filter((item) => !item.pull_request);
    githubState = {
      status: "LIVE",
      repo: REPO,
      openIssues: realIssues.length,
      openPullRequests: pulls.length,
      mainSha: main.sha,
      pushedAt: repository.pushed_at,
      tracked: realIssues
        .filter((item) => [20, 17, 8, 9, 7].includes(item.number))
        .map((item) => ({
          number: item.number,
          title: item.title,
          state: item.state,
          updatedAt: item.updated_at
        })),
      pullRequests: pulls
        .filter((item) => item.number === 19)
        .map((item) => ({
          number: item.number,
          title: item.title,
          state: item.state,
          draft: item.draft,
          updatedAt: item.updated_at
        }))
    };
  } catch (error) {
    githubState.error = error.message;
  }

  return res.status(200).json({
    version: "control-state-v1",
    generatedAt,
    exposure: "PUBLIC_SANITIZED",
    focus: {
      product: "ERP Food Control",
      state: "ACTIVE",
      northStar: "Pedido/PDV → Pagamento/Caixa → Fiscal → Entrega → Financeiro → Contábil",
      privateDetails: "LOCKED",
      lanes: [
        { order: 1, name: "PDV reliability + idempotency", state: "ACTIVE" },
        { order: 2, name: "Cashier truth + daily boundary", state: "NEXT" },
        { order: 3, name: "Financial event contract", state: "NEXT" },
        { order: 4, name: "Payments / cash / change", state: "QUEUED" },
        { order: 5, name: "Order integrity + delivery", state: "QUEUED" },
        { order: 6, name: "Fiscal / NF-e / NFC-e / XML", state: "QUEUED" },
        { order: 7, name: "Financeiro + Contábil", state: "QUEUED" }
      ]
    },
    sources: {
      github: githubState,
      brain: {
        status: "PRIVATE_LOCKED",
        mode: "server-side adapter required",
        publicContentExposed: false
      },
      drive: {
        status: "PRIVATE_LOCKED",
        mode: "server-side OAuth adapter required",
        publicContentExposed: false
      },
      auditor: {
        status: "PLANNED",
        name: "Independent adversarial auditor / Claude Code adapter",
        connected: false
      }
    },
    submarine: {
      mode: "OFF",
      writeAuthority: false,
      wipLimit: 1,
      pipeline: [
        "ticket",
        "mission envelope",
        "executor",
        "tests",
        "adversarial audit",
        "evidence",
        "Draft PR",
        "Human Review"
      ],
      humanGates: ["merge", "deploy", "production", "live database", "secrets"]
    },
    security: {
      privateDataExposed: false,
      browserSecrets: false,
      writeEndpointsEnabled: false,
      note: "Public endpoint intentionally exposes only sanitized operational state."
    }
  });
};
