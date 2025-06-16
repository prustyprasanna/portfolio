document.addEventListener('DOMContentLoaded', function() {
    const startButtons = document.querySelectorAll('.start-assessment');
    
    startButtons.forEach(button => {
        button.addEventListener('click', function() {
            const skillId = this.dataset.skillId;
            startAssessment(skillId);
        });
    });
});

function startAssessment(skillId) {
    // Mock assessment for now
    const score = Math.floor(Math.random() * 41) + 60; // Score between 60-100
    
    fetch('/skills-assessment/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            skill_id: skillId,
            score: score
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

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
    return cookieValue;
}