// Assessment Management System - Main JavaScript

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Assessment timer functionality
    if ($('#assessment-timer').length) {
        initializeTimer();
    }

    // Question navigation
    if ($('.question-navigation').length) {
        initializeQuestionNavigation();
    }

    // Auto-save answers
    if ($('.answer-form').length) {
        initializeAutoSave();
    }

    // Form validation
    initializeFormValidation();
});

// Timer functionality
function initializeTimer() {
    const timerElement = $('#assessment-timer');
    const timeLimit = parseInt(timerElement.data('time-limit'));
    const sessionId = timerElement.data('session-id');
    
    let remainingTime = timeLimit * 60; // Convert to seconds
    
    function updateTimer() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        
        timerElement.text(`${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
        
        // Update timer color based on remaining time
        timerElement.removeClass('warning danger');
        if (remainingTime <= 300) { // 5 minutes
            timerElement.addClass('danger');
        } else if (remainingTime <= 600) { // 10 minutes
            timerElement.addClass('warning');
        }
        
        if (remainingTime <= 0) {
            // Time's up - auto-submit
            alert('Time is up! Your assessment will be submitted automatically.');
            window.location.href = `/assessments/submit-assessment/${sessionId}/`;
            return;
        }
        
        remainingTime--;
    }
    
    // Update timer every second
    setInterval(updateTimer, 1000);
    updateTimer(); // Initial call
}

// Question navigation
function initializeQuestionNavigation() {
    $('.question-nav-btn').click(function(e) {
        e.preventDefault();
        const questionId = $(this).data('question-id');
        const questionElement = $(`#question-${questionId}`);
        
        // Hide all questions
        $('.question-card').hide();
        
        // Show selected question
        questionElement.show();
        
        // Update active navigation button
        $('.question-nav-btn').removeClass('active');
        $(this).addClass('active');
    });
}

// Auto-save answers
function initializeAutoSave() {
    let saveTimeout;
    
    $('.answer-input').on('input', function() {
        clearTimeout(saveTimeout);
        
        saveTimeout = setTimeout(function() {
            saveAnswer();
        }, 2000); // Save after 2 seconds of inactivity
    });
    
    function saveAnswer() {
        const formData = $('.answer-form').serialize();
        const sessionId = $('.answer-form').data('session-id');
        
        $.ajax({
            url: '/assessments/ajax/save-answer/',
            method: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    showNotification('Answer saved automatically', 'success');
                }
            },
            error: function() {
                showNotification('Failed to save answer', 'error');
            }
        });
    }
}

// Form validation
function initializeFormValidation() {
    $('form').on('submit', function(e) {
        const requiredFields = $(this).find('[required]');
        let isValid = true;
        
        requiredFields.each(function() {
            if (!$(this).val().trim()) {
                isValid = false;
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Please fill in all required fields', 'error');
        }
    });
}

// Progress bar update
function updateProgress(answered, total) {
    const percentage = (answered / total) * 100;
    $('.progress-bar').css('width', percentage + '%');
    $('.progress-text').text(`${answered}/${total} questions answered`);
}

// Show notification
function showNotification(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : 
                      type === 'success' ? 'alert-success' : 'alert-info';
    
    const notification = $(`
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('.container').first().prepend(notification);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        notification.alert('close');
    }, 5000);
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    
    // Fallback to meta tag if cookie not found
    if (!cookieValue && name === 'csrftoken') {
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) {
            cookieValue = metaTag.getAttribute('content');
        }
    }
    
    return cookieValue;
}

// Export functionality
function exportData(format, url) {
    window.location.href = `${url}?format=${format}`;
}

// Bulk actions
function performBulkAction(action, selectedIds) {
    if (selectedIds.length === 0) {
        showNotification('Please select items to perform this action', 'error');
        return;
    }
    
    if (confirm(`Are you sure you want to ${action} the selected items?`)) {
        $.ajax({
            url: '/assessments/bulk-action/',
            method: 'POST',
            data: {
                action: action,
                ids: selectedIds,
                csrfmiddlewaretoken: getCookie('csrftoken')
            },
            success: function(response) {
                if (response.success) {
                    showNotification(`${action} completed successfully`, 'success');
                    location.reload();
                } else {
                    showNotification(response.error, 'error');
                }
            },
            error: function() {
                showNotification('An error occurred while performing the action', 'error');
            }
        });
    }
}

// Search functionality
function initializeSearch() {
    let searchTimeout;
    
    $('.search-input').on('input', function() {
        clearTimeout(searchTimeout);
        
        searchTimeout = setTimeout(function() {
            const query = $('.search-input').val();
            const currentUrl = new URL(window.location);
            currentUrl.searchParams.set('search', query);
            window.location.href = currentUrl.toString();
        }, 500);
    });
}

// Modal functionality
function showModal(title, content, size = 'modal-lg') {
    const modal = $(`
        <div class="modal fade" tabindex="-1">
            <div class="modal-dialog ${size}">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                </div>
            </div>
        </div>
    `);
    
    $('body').append(modal);
    modal.modal('show');
    
    modal.on('hidden.bs.modal', function() {
        modal.remove();
    });
}

// Chart functionality (if Chart.js is available)
function initializeCharts() {
    if (typeof Chart !== 'undefined') {
        // Assessment performance chart
        const ctx = document.getElementById('performanceChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'Average Score',
                        data: chartData.scores,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
    }
}

// Print functionality
function printAssessment(sessionId) {
    const printWindow = window.open(`/assessments/print-assessment/${sessionId}/`, '_blank');
    printWindow.onload = function() {
        printWindow.print();
    };
}

// Confirm delete functionality
function confirmDelete(itemName, itemUrl) {
    if (confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
        // For now, redirect to the item detail page
        // In a full implementation, this would make a DELETE request
        window.location.href = itemUrl;
    }
}

// Keyboard shortcuts
$(document).keydown(function(e) {
    // Ctrl+S to save
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        if ($('.answer-form').length) {
            $('.answer-form').submit();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        $('.modal').modal('hide');
    }
}); f u n c t i o n   c o n f i r m D e l e t e ( i t e m N a m e ,   i t e m U r l )   {   i f   ( c o n f i r m ( ' A r e   y o u   s u r e   y o u   w a n t   t o   d e l e t e   \  
   +   i t e m N a m e   +    
 \ ?   T h i s   a c t i o n   c a n n o t   b e   u n d o n e . ' ) )   {   w i n d o w . l o c a t i o n . h r e f   =   i t e m U r l ;   }   }  
 