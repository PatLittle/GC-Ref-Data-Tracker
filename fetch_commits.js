const fs = require('fs');
const fetch = require('node-fetch');
const path = require('path');

// Environment variables
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO_OWNER = 'PatLittle';
const REPO_NAME = 'GC-Ref-Data-Tracker';
const BRANCH_NAME = 'main';
const OUTPUT_FILE = 'docs/commits.json'; // Location to store the fetched commit data

// GitHub API URL for fetching commits
const GITHUB_API_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits?sha=${BRANCH_NAME}&per_page=500`;

// Fetch commit details (including diffs) for a given commit SHA
async function fetchCommitDetails(commitSha) {
  const commitApiUrl = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits/${commitSha}`;
  const response = await fetch(commitApiUrl, {
    headers: {
      'Authorization': `token ${GITHUB_TOKEN}`,
      'Accept': 'application/vnd.github.v3+json'
    }
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch commit details for ${commitSha}: ${response.statusText}`);
  }

  const commitData = await response.json();
  return commitData;
}

// Fetch commits and their diffs
async function fetchCommits() {
  try {
    const response = await fetch(GITHUB_API_URL, {
      headers: {
        'Authorization': `token ${GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    });

    if (!response.ok) {
      throw new Error(`GitHub API responded with ${response.status}: ${response.statusText}`);
    }

    const commits = await response.json();
    console.log(`Fetched ${commits.length} commits.`);

    // Array to hold the fetched commits with diffs
    const detailedCommits = [];

    // Fetch commit details (including diffs) for each commit
    for (const commit of commits) {
      const commitSha = commit.sha;
      console.log(`Fetching details for commit ${commitSha}`);
      const commitDetails = await fetchCommitDetails(commitSha);
      
      // Add the commit details (including diffs) to the detailedCommits array
      detailedCommits.push(commitDetails);
    }

    // Write the detailed commits (with diffs) to a JSON file
    fs.mkdirSync(path.dirname(OUTPUT_FILE), { recursive: true });
    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(detailedCommits, null, 2));
    console.log(`Commit data with diffs saved to ${OUTPUT_FILE}`);
  } catch (error) {
    console.error('Error fetching commits:', error);
    process.exit(1); // Exit with failure
  }
}

// Run the fetchCommits function
fetchCommits();
