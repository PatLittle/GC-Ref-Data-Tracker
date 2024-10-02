import fetch from 'node-fetch'; // Use import instead of require
import fs from 'fs';
import { promisify } from 'util';

const writeFileAsync = promisify(fs.writeFile);

// Environment variables
const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const REPO_OWNER = 'PatLittle';
const REPO_NAME = 'GC-Ref-Data-Tracker';
const BRANCH_NAME = 'main';
const OUTPUT_FILE = './build/commits.json'; // Location to store the fetched commit data

const GITHUB_API_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/commits?sha=${BRANCH_NAME}&per_page=50`;

// Fetch commits from GitHub
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

    await writeFileAsync(OUTPUT_FILE, JSON.stringify(commits, null, 2));
    console.log(`Commit data saved to ${OUTPUT_FILE}`);
  } catch (error) {
    console.error('Error fetching commits:', error);
    process.exit(1); // Exit with failure
  }
}

fetchCommits();
