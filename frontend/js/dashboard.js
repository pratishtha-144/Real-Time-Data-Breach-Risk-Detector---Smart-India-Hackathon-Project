/**
 * Dashboard JavaScript
 * Handles API calls, UI updates, and real-time data display
 */

// API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// DOM Elements
const scanBtn = document.getElementById('scanBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const riskBadge = document.getElementById('riskBadge');
const riskLevelText = document.getElementById('riskLevelText');
const riskScore = document.getElementById('riskScore');
const lastScanTime = document.getElementById('lastScanTime');
const criticalCount = document.getElementById('criticalCount');
const warningCount = document.getElementById('warningCount');
const infoCount = document.getElementById('infoCount');
const issuesCount = document.getElementById('issuesCount');
const issuesList = document.getElementById('issuesList');
const recommendationsList = document.getElementById('recommendationsList');

// Event Listeners
scanBtn.addEventListener('click', runSecurityScan);

// Initialize dashboard on load
window.addEventListener('load', () => {
    loadLatestData();
});

/**
 * Run a new security scan
 */
async function runSecurityScan() {
    try {
        // Show loading overlay
        showLoading();

        // Call scan API
        const response = await fetch(`${API_BASE_URL}/scan`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Scan failed');
        }

        const data = await response.json();

        // Update dashboard with results
        updateDashboard(data);

        // Show success notification
        showToast('Security scan completed successfully!', 'success');

    } catch (error) {
        console.error('Error running scan:', error);
        showToast('Failed to run security scan. Make sure the backend is running.', 'error');
    } finally {
        hideLoading();
    }
}

/**
 * Load latest scan data on page load
 */
async function loadLatestData() {
    try {
        const response = await fetch(`${API_BASE_URL}/risk`);

        if (!response.ok) {
            return; // No data available yet
        }

        const riskData = await response.json();

        if (riskData.risk_level === 'UNKNOWN') {
            return; // No scans performed yet
        }

        // Update basic risk info
        updateRiskDisplay(riskData.risk_level, riskData.risk_score, riskData.last_scan);

    } catch (error) {
        console.error('Error loading data:', error);
    }
}

/**
 * Update the entire dashboard with scan results
 */
function updateDashboard(scanData) {
    // Update risk display
    updateRiskDisplay(
        scanData.risk_level,
        scanData.risk_score,
        new Date().toISOString()
    );

    // Update alert counts
    updateAlertCounts(scanData.alert_summary);

    // Update issues list
    updateIssuesList(scanData.all_issues);

    // Update recommendations
    updateRecommendations(scanData.recommendations);
}

/**
 * Update the risk level display
 */
function updateRiskDisplay(level, score, timestamp) {
    // Update risk level badge
    riskBadge.className = 'risk-level-badge ' + level.toLowerCase();
    riskLevelText.textContent = level;

    // Update risk score
    riskScore.textContent = score;

    // Update risk icon based on level
    const riskIcon = riskBadge.querySelector('.risk-icon');
    const icons = {
        'LOW': '🟢',
        'MEDIUM': '🟡',
        'HIGH': '🟠',
        'CRITICAL': '🔴',
        'UNKNOWN': '⚪'
    };
    riskIcon.textContent = icons[level] || '⚪';

    // Update last scan time
    if (timestamp) {
        const date = new Date(timestamp);
        lastScanTime.textContent = `Last scan: ${date.toLocaleString()}`;
    }
}

/**
 * Update alert count statistics
 */
function updateAlertCounts(alertSummary) {
    criticalCount.textContent = alertSummary.CRITICAL || 0;
    warningCount.textContent = alertSummary.WARNING || 0;
    infoCount.textContent = alertSummary.INFO || 0;
}

/**
 * Update the issues list
 */
function updateIssuesList(issues) {
    // Update issues count badge
    issuesCount.textContent = `${issues.length} ${issues.length === 1 ? 'Issue' : 'Issues'}`;

    if (issues.length === 0) {
        issuesList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">✅</div>
                <p>No security issues detected</p>
                <p class="empty-subtext">Your system looks secure!</p>
            </div>
        `;
        return;
    }

    // Clear existing issues
    issuesList.innerHTML = '';

    // Add each issue
    issues.forEach(issue => {
        const issueItem = createIssueElement(issue);
        issuesList.appendChild(issueItem);
    });
}

/**
 * Create an issue HTML element
 */
function createIssueElement(issue) {
    const div = document.createElement('div');
    div.className = `issue-item ${issue.severity.toLowerCase()}`;

    div.innerHTML = `
        <div class="issue-header">
            <span class="issue-type">${formatIssueType(issue.type)}</span>
            <span class="issue-severity ${issue.severity.toLowerCase()}">${issue.severity}</span>
        </div>
        <div class="issue-description">${issue.description}</div>
    `;

    // Add animation
    div.style.opacity = '0';
    div.style.transform = 'translateY(10px)';
    setTimeout(() => {
        div.style.transition = 'all 0.3s ease';
        div.style.opacity = '1';
        div.style.transform = 'translateY(0)';
    }, 10);

    return div;
}

/**
 * Format issue type for display
 */
function formatIssueType(type) {
    return type.split('_').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
}

/**
 * Update recommendations list
 */
function updateRecommendations(recommendations) {
    if (recommendations.length === 0) {
        recommendationsList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">✅</div>
                <p>No specific recommendations at this time</p>
                <p class="empty-subtext">Keep up the good security practices!</p>
            </div>
        `;
        return;
    }

    // Clear existing recommendations
    recommendationsList.innerHTML = '';

    // Add each recommendation
    recommendations.forEach((rec, index) => {
        const recItem = document.createElement('div');
        recItem.className = 'recommendation-item';
        recItem.textContent = rec;

        // Add staggered animation
        recItem.style.opacity = '0';
        recItem.style.transform = 'translateX(-10px)';
        setTimeout(() => {
            recItem.style.transition = 'all 0.3s ease';
            recItem.style.opacity = '1';
            recItem.style.transform = 'translateX(0)';
        }, index * 50);

        recommendationsList.appendChild(recItem);
    });
}

/**
 * Show loading overlay
 */
function showLoading() {
    loadingOverlay.classList.remove('hidden');
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    setTimeout(() => {
        loadingOverlay.classList.add('hidden');
    }, 300);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toastContainer');

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    // Auto-remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 3000);
}

/**
 * Format timestamp for display
 */
function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Export functions for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        runSecurityScan,
        updateDashboard,
        formatIssueType
    };
}
