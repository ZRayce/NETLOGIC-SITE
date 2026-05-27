document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const alertTitle = document.getElementById("status-title");
    const alertDesc = document.getElementById("status-desc");

    function updateTerminalStatus(message, details, isSuccess = false) {
        if (!alertTitle || !alertDesc) return;
        alertTitle.textContent = isSuccess ? `[SUCCESS] ${message}` : `[CRITICAL_FAULT] ${message}`;
        alertDesc.textContent = details;
    }

    // --- Login Submission Pipeline ---
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault(); // Safely intercepts native action so Enter key works perfectly
            
            const username = document.getElementById("loginUsername").value.trim();
            const password = document.getElementById("loginPassword").value;
            const csrfToken = document.getElementById("csrf_token").value;

            updateTerminalStatus("VERIFYING_IDENTITY", "Processing handshake request vectors...", true);

            fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || "Authentication perimeter handshake failed.");
                return data;
            })
            .then(data => {
                updateTerminalStatus("ACCESS_GRANTED", "Identity unsealed. Launching terminal session...", true);
                
                // FIXED: Boot transition engine now holds execution priority
                setTimeout(() => {
                    executeBootTransition();
                }, 500);
            })
            .catch(err => {
                updateTerminalStatus("AUTH_REJECTED", err.message, false);
            });
        });
    }

    // --- Registration Submission Pipeline ---
    if (registerForm) {
        registerForm.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const username = document.getElementById("regUsername").value.trim();
            const email = document.getElementById("regEmail").value.trim();
            const password = document.getElementById("regPassword").value;
            const csrfToken = document.getElementById("csrf_token").value;

            updateTerminalStatus("PROVISIONING_NODE", "Injecting cryptographic data-blocks into local ledger...", true);

            fetch("/api/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({ username: username, email: email, password: password })
            })
            .then(async response => {
                const data = await response.json();
                if (!response.ok) throw new Error(data.error || "Registration block rejected by kernel check.");
                return data;
            })
            .then(data => {
                updateTerminalStatus("PROVISION_COMPLETE", "Node committed successfully. Initializing verification return...", true);
                setTimeout(() => {
                    const toggleBtn = document.getElementById("toggle-to-login");
                    if (toggleBtn) toggleBtn.click();
                    
                    const loginUserField = document.getElementById("loginUsername");
                    if (loginUserField) loginUserField.value = username;
                }, 1500);
            })
            .catch(err => {
                updateTerminalStatus("REGISTRATION_FAULT", err.message, false);
            });
        });
    }
});

// High-Retention Terminal Initialization Boot Transition Engine
function executeBootTransition() {
    const overlay = document.getElementById("boot-overlay");
    const stream = document.getElementById("boot-log-stream");
    if (!overlay || !stream) {
        window.location.href = "/";
        return;
    }

    // Activate dark fullscreen initialization layer
    overlay.classList.remove("hidden");

    const bootSequences = [
        "ALLOCATING VM CORE CONDUITS... [OK]",
        "MOUNTING DATABASE KERNEL ENGINE LAYER... [OK]",
        "UNSEALING OPERATOR STORAGE LEDGER SCHEMAS... [OK]",
        "ESTABLISHING LOCALHOST LOOPBACK ADDRESS BINDINGS... [OK]",
        "SYNCING METRICS // DAILY_STREAK INTERCONNECTS... [OK]",
        "LOADING IPV4 & IPV6 BITWISE SUB-MASK SHIFTERS... [OK]",
        "INITIALIZING CISCO COMMAND REGEX INTERPRETER CORE... [OK]",
        "PARSING RJ45 / HARDWARE WIRE SCHEMATICS PROFILES... [OK]",
        "BUILDING DISPATCH INTERFACE PANEL VIEWPORT SCAPE... [OK]",
        "SECURITY HANDSHAKE COMPLETION VALIDATED.",
        "LAUNCHING NETLOGIC MAIN OPERATIONAL DESKTOP HUB..."
    ];

    let currentLine = 0;

    function printNextBootLine() {
        if (currentLine < bootSequences.length) {
            const p = document.createElement("p");
            const time = new Date().toLocaleTimeString('en-GB', { hour12: false });
            
            // Highlight the final activation metrics in mint green
            if (currentLine >= bootSequences.length - 2) {
                p.className = "text-[#4ade80] font-bold";
            }
            
            p.textContent = `[${time}] ${bootSequences[currentLine]}`;
            stream.appendChild(p);
            
            // Auto scroll container downward
            stream.scrollTop = stream.scrollHeight;
            currentLine++;
            
            let dynamicInterval = Math.floor(Math.random() * 100) + 40; // Blazing fast layout generation metrics
            setTimeout(printNextBootLine, dynamicInterval);
        } else {
            // FIXED: Redirection happens strictly AFTER the ticker log completes entirely
            setTimeout(() => {
                window.location.href = "/";
            }, 600);
        }
    }

    printNextBootLine();
}