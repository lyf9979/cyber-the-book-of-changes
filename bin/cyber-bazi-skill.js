#!/usr/bin/env node

const fs = require("fs");
const path = require("path");
const os = require("os");

const repoRoot = path.resolve(__dirname, "..");
const defaultName = "cyber-bazi-divination";
const copyItems = [
  "skill",
  "references",
  "examples",
  "docs",
  "scripts",
  "AGENTS.md",
  "README.md",
  "LICENSE",
  "CONTRIBUTING.md",
  "CONTRIBUTORS.md"
];

const targetRoots = {
  claude: path.join(os.homedir(), ".claude", "skills"),
  codex: path.join(os.homedir(), ".codex", "skills")
};

function printHelp() {
  console.log(
    [
      "Cyber Bazi Skill CLI",
      "",
      "Usage:",
      "  cyber-bazi-skill install [--target claude|codex|all] [--name NAME] [--source PATH] [--force]",
      "  cyber-bazi-skill list-targets",
      "",
      "Examples:",
      "  npx cyber-bazi-skill install --target claude",
      "  npx github:lyf9979/cyber-the-book-of-changes install --target all",
      "  npx cyber-bazi-skill install --target codex --name cyber-bazi-divination --force"
    ].join("\n")
  );
}

function parseArgs(argv) {
  const args = {
    command: argv[0] || "",
    target: "claude",
    name: defaultName,
    source: repoRoot,
    force: false
  };

  for (let i = 1; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--target") {
      args.target = argv[i + 1] || args.target;
      i += 1;
    } else if (part === "--name") {
      args.name = argv[i + 1] || args.name;
      i += 1;
    } else if (part === "--source") {
      args.source = path.resolve(argv[i + 1] || args.source);
      i += 1;
    } else if (part === "--force") {
      args.force = true;
    } else if (part === "--help" || part === "-h") {
      args.command = "help";
    }
  }

  return args;
}

function ensureExists(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`Missing required path: ${filePath}`);
  }
}

function copyItem(sourceRoot, item, destinationRoot) {
  const sourcePath = path.join(sourceRoot, item);
  const destinationPath = path.join(destinationRoot, item);
  ensureExists(sourcePath);
  fs.mkdirSync(path.dirname(destinationPath), { recursive: true });
  fs.cpSync(sourcePath, destinationPath, { recursive: true });
}

function installToTarget(sourceRoot, target, name, force) {
  const root = targetRoots[target];
  if (!root) {
    throw new Error(`Unsupported target: ${target}`);
  }

  const destination = path.join(root, name);
  fs.mkdirSync(root, { recursive: true });

  if (fs.existsSync(destination)) {
    if (!force) {
      throw new Error(
        `Destination already exists: ${destination}\nUse --force to overwrite.`
      );
    }
    fs.rmSync(destination, { recursive: true, force: true });
  }

  fs.mkdirSync(destination, { recursive: true });
  copyItems.forEach((item) => copyItem(sourceRoot, item, destination));
  return destination;
}

function run() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.command || args.command === "help") {
    printHelp();
    return;
  }

  if (args.command === "list-targets") {
    Object.entries(targetRoots).forEach(([key, value]) => {
      console.log(`${key}: ${value}`);
    });
    return;
  }

  if (args.command !== "install") {
    throw new Error(`Unknown command: ${args.command}`);
  }

  const targets =
    args.target === "all" ? Object.keys(targetRoots) : [args.target];
  targets.forEach((target) => {
    const installedPath = installToTarget(
      args.source,
      target,
      args.name,
      args.force
    );
    console.log(`[ok] Installed for ${target}: ${installedPath}`);
  });
}

try {
  run();
} catch (error) {
  console.error(`[error] ${error.message}`);
  process.exitCode = 1;
}

