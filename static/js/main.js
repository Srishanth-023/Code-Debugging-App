// Main JavaScript for Code Debugging App

document.addEventListener('DOMContentLoaded', function() {
    // Initialize code editors
    initializeCodeEditors();
    
    // Initialize other components
    initializeTooltips();
    initializeAlerts();
});

// Code Editor Functionality
function initializeCodeEditors() {
    const codeEditors = document.querySelectorAll('.code-editor-textarea');
    
    codeEditors.forEach(function(textarea) {
        const editor = CodeMirror.fromTextArea(textarea, {
            lineNumbers: true,
            mode: 'python',
            theme: 'monokai',
            indentUnit: 4,
            indentWithTabs: false,
            lineWrapping: true,
            matchBrackets: true,
            autoCloseBrackets: true,
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
            extraKeys: {
                "Ctrl-Space": "autocomplete",
                "Ctrl-Enter": function(cm) {
                    executeCode(cm.getValue());
                },
                "F11": function(cm) {
                    cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                },
                "Esc": function(cm) {
                    if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
                }
            }
        });
        
        // Store editor instance for later use
        textarea.codeMirrorInstance = editor;
        
        // Add toolbar functionality
        setupEditorToolbar(editor, textarea.closest('.code-editor-container'));
    });
}

function setupEditorToolbar(editor, container) {
    const toolbar = container.querySelector('.code-editor-toolbar');
    if (!toolbar) return;
    
    // Run button
    const runBtn = toolbar.querySelector('.btn-run');
    if (runBtn) {
        runBtn.addEventListener('click', function() {
            executeCode(editor.getValue());
        });
    }
    
    // Reset button
    const resetBtn = toolbar.querySelector('.btn-reset');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (confirm('Are you sure you want to reset the code?')) {
                const originalCode = editor.getTextArea().getAttribute('data-original-code');
                if (originalCode) {
                    editor.setValue(originalCode);
                }
            }
        });
    }
    
    // Submit button
    const submitBtn = toolbar.querySelector('.btn-submit');
    if (submitBtn) {
        submitBtn.addEventListener('click', function() {
            const challengeId = submitBtn.getAttribute('data-challenge-id');
            if (challengeId) {
                submitSolution(challengeId, editor.getValue());
            }
        });
    }
    
    // Fullscreen button
    const fullscreenBtn = toolbar.querySelector('.btn-fullscreen');
    if (fullscreenBtn) {
        fullscreenBtn.addEventListener('click', function() {
            editor.setOption("fullScreen", !editor.getOption("fullScreen"));
        });
    }
}

// Code Execution
async function executeCode(code) {
    if (!code.trim()) {
        showAlert('Please enter some code to execute.', 'warning');
        return;
    }
    
    const outputPanel = document.getElementById('output-panel');
    const outputContent = document.getElementById('output-content');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    if (!outputPanel || !outputContent) {
        console.error('Output panel not found');
        return;
    }
    
    // Show loading state
    showLoadingState(true);
    outputPanel.style.display = 'block';
    outputContent.textContent = 'Executing code...';
    outputPanel.className = 'output-panel';
    
    try {
        const response = await fetch('/challenges/execute/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        // Display results
        displayExecutionResult(result);
        
    } catch (error) {
        displayExecutionResult({
            output: '',
            error: 'Network error: ' + error.message
        });
    } finally {
        showLoadingState(false);
    }
}

function displayExecutionResult(result) {
    const outputPanel = document.getElementById('output-panel');
    const outputContent = document.getElementById('output-content');
    
    if (!outputPanel || !outputContent) return;
    
    let output = '';
    let panelClass = 'output-panel';
    
    if (result.error) {
        output = 'Error:\n' + result.error;
        if (result.output) {
            output = 'Output:\n' + result.output + '\n\n' + output;
        }
        panelClass += ' error';
    } else if (result.output) {
        output = result.output;
        panelClass += ' success';
    } else {
        output = 'Code executed successfully (no output)';
        panelClass += ' success';
    }
    
    outputContent.textContent = output;
    outputPanel.className = panelClass;
    outputPanel.style.display = 'block';
}

// Solution Submission
async function submitSolution(challengeId, code) {
    if (!code.trim()) {
        showAlert('Please enter your solution code before submitting.', 'warning');
        return;
    }
    
    if (!confirm('Are you sure you want to submit this solution?')) {
        return;
    }
    
    showLoadingState(true);
    
    try {
        const response = await fetch(`/challenges/submit/${challengeId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displaySubmissionResult(result);
        } else {
            showAlert(result.error || 'Submission failed', 'danger');
        }
        
    } catch (error) {
        showAlert('Network error: ' + error.message, 'danger');
    } finally {
        showLoadingState(false);
    }
}

function displaySubmissionResult(result) {
    const outputPanel = document.getElementById('output-panel');
    const outputContent = document.getElementById('output-content');
    
    let message = '';
    let alertType = '';
    let panelClass = 'output-panel';
    
    if (result.status === 'correct') {
        message = `🎉 Correct! You earned ${result.points_earned} points!`;
        alertType = 'success';
        panelClass += ' success';
    } else if (result.status === 'incorrect') {
        message = '❌ Incorrect solution. Please try again.';
        alertType = 'warning';
        panelClass += ' error';
    } else {
        message = '⚠️ There was an issue with your submission.';
        alertType = 'warning';
        panelClass += ' error';
    }
    
    // Show alert
    showAlert(message, alertType);
    
    // Show output in panel
    if (outputPanel && outputContent) {
        let output = 'Submission Result:\n' + message + '\n\n';
        
        if (result.output) {
            output += 'Your Output:\n' + result.output;
        }
        
        if (result.error) {
            output += '\n\nError:\n' + result.error;
        }
        
        outputContent.textContent = output;
        outputPanel.className = panelClass;
        outputPanel.style.display = 'block';
    }
    
    // Refresh page after successful submission to update progress
    if (result.status === 'correct') {
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    }
}

// Utility Functions
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.split('; ')
               .find(row => row.startsWith('csrftoken='))
               ?.split('=')[1] || '';
}

function showLoadingState(show) {
    const loadingSpinner = document.getElementById('loading-spinner');
    const runButtons = document.querySelectorAll('.btn-run, .btn-submit');
    
    if (loadingSpinner) {
        loadingSpinner.style.display = show ? 'block' : 'none';
    }
    
    runButtons.forEach(btn => {
        btn.disabled = show;
        if (show) {
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status"></span> Running...';
        } else {
            if (btn.classList.contains('btn-run')) {
                btn.innerHTML = '<i class="fas fa-play"></i> Run Code';
            } else if (btn.classList.contains('btn-submit')) {
                btn.innerHTML = '<i class="fas fa-check"></i> Submit Solution';
            }
        }
    });
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert alert at the top of the main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.insertBefore(alertDiv, mainContent.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function initializeTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializeAlerts() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    });
}

// Challenge Navigation
function navigateToChallenge(challengeId) {
    window.location.href = `/challenges/challenge/${challengeId}/`;
}

function navigateToWeek(weekNumber) {
    window.location.href = `/challenges/week/${weekNumber}/`;
}

// Export functions for global use
window.executeCode = executeCode;
window.submitSolution = submitSolution;
window.navigateToChallenge = navigateToChallenge;
window.navigateToWeek = navigateToWeek;