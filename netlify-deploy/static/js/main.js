// Academic Tab Functionality
document.addEventListener('DOMContentLoaded', function() {
  // Initialize academic tab functionality if elements exist
  if (document.getElementById('academic-tab-content')) {
    initAcademicTab();
  }
});

function initAcademicTab() {
  // Course tracking functionality
  initCourseTracker();
  
  // Academic calendar functionality
  initAcademicCalendar();
  
  // Initialize performance insights
  updatePerformanceInsights();
  
  // Initialize security and data privacy options
  initSecuritySettings();
  
  // Crisis detection simulation (for demo purposes)
  setupCrisisDetection();
}

function initCourseTracker() {
  // Add course button functionality
  const addCourseBtn = document.querySelector('.add-course-btn');
  if (addCourseBtn) {
    addCourseBtn.addEventListener('click', function() {
      // Modal would go here in a full implementation
      alert('This would open a form to add a new course. In a real implementation, this would be a modal with a form.');
    });
  }
  
  // Initialize course progress bars
  const progressBars = document.querySelectorAll('.progress-bar');
  progressBars.forEach(bar => {
    const progress = bar.getAttribute('data-progress');
    bar.style.width = `${progress}%`;
  });
  
  // Semester selector functionality
  const semesterSelectors = document.querySelectorAll('.semester-selector select');
  semesterSelectors.forEach(selector => {
    selector.addEventListener('change', function() {
      // In a real implementation, this would fetch data for the selected semester
      console.log('Selected semester:', this.value);
      // Mock data update
      if (this.value === 'Spring 2023') {
        document.querySelector('.stat-value.gpa').textContent = '3.7';
      } else if (this.value === 'Fall 2022') {
        document.querySelector('.stat-value.gpa').textContent = '3.5';
      } else {
        document.querySelector('.stat-value.gpa').textContent = '3.8';
      }
    });
  });
}

function initAcademicCalendar() {
  // Calendar navigation
  const prevBtn = document.querySelector('.calendar-nav.prev');
  const nextBtn = document.querySelector('.calendar-nav.next');
  const calendarTitle = document.querySelector('.calendar-title');
  
  let currentDate = new Date();
  updateCalendarHeader();
  
  if (prevBtn && nextBtn && calendarTitle) {
    prevBtn.addEventListener('click', function() {
      currentDate.setMonth(currentDate.getMonth() - 1);
      updateCalendarHeader();
    });
    
    nextBtn.addEventListener('click', function() {
      currentDate.setMonth(currentDate.getMonth() + 1);
      updateCalendarHeader();
    });
  }
  
  function updateCalendarHeader() {
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December'];
    if (calendarTitle) {
      calendarTitle.textContent = `${months[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
    }
    // In a real implementation, this would also update the calendar grid
  }
}

function updatePerformanceInsights() {
  // This would normally analyze real data from the user's academic performance
  // and journal entries to provide personalized insights
  
  // For demonstration, we're just setting up some predefined insights
  const insightsContainer = document.querySelector('.insights-container');
  
  // In a real implementation, these insights would be dynamically generated
  // based on the user's actual data and performance patterns
}

function initSecuritySettings() {
  // Toggle security settings
  const securityToggles = document.querySelectorAll('.security-toggle');
  securityToggles.forEach(toggle => {
    toggle.addEventListener('change', function() {
      const setting = this.getAttribute('data-setting');
      const isEnabled = this.checked;
      console.log(`Security setting ${setting} is now ${isEnabled ? 'enabled' : 'disabled'}`);
      
      // Show verification confirmation for certain settings
      if (setting === 'uf_verification' && isEnabled) {
        // In a real implementation, this would trigger the UF verification process
        alert('This would initiate the UF student verification process using your GatorLink credentials.');
      }
    });
  });
}

function setupCrisisDetection() {
  // This is a simulation of the crisis detection feature for demonstration purposes
  // In a real implementation, this would analyze journal entries, academic performance,
  // and other data points to detect potential crisis situations
  
  const crisisAlert = document.querySelector('.crisis-alert');
  const closeBtn = document.querySelector('.crisis-close');
  
  if (crisisAlert && closeBtn) {
    // Set up the close button
    closeBtn.addEventListener('click', function() {
      crisisAlert.classList.remove('active');
    });
    
    // Demo function to show crisis alert
    // In a real implementation, this would be triggered by the system's analysis
    setTimeout(() => {
      // This simulates the system detecting a potential crisis based on data analysis
      // For demo purposes, we're showing it after a delay
      crisisAlert.classList.add('active');
    }, 60000); // Show after 1 minute for demo purposes
    
    // Set up action buttons
    const contactBtn = document.querySelector('.crisis-btn.primary');
    if (contactBtn) {
      contactBtn.addEventListener('click', function() {
        // In a real implementation, this would connect to UF's counseling services
        window.open('https://counseling.ufl.edu/', '_blank');
        crisisAlert.classList.remove('active');
      });
    }
  }
}

// Function to analyze academic performance and mood correlation
function analyzePerformanceMoodCorrelation() {
  // In a real implementation, this would analyze journal entries and academic data
  // to find correlations between mood and academic performance
  
  // Mock data analysis for demonstration
  return {
    positiveCorrelations: [
      { mood: 'Energetic', performance: 'Higher assignment completion rate' },
      { mood: 'Focused', performance: 'Better exam scores' }
    ],
    negativeCorrelations: [
      { mood: 'Anxious', performance: 'Lower quiz scores' },
      { mood: 'Tired', performance: 'Missed assignments' }
    ]
  };
}

// Function to generate study recommendations based on performance data
function generateStudyRecommendations() {
  // In a real implementation, this would analyze various data points
  // to provide personalized study recommendations
  
  // Mock recommendations for demonstration
  return [
    { 
      course: 'Computer Science',
      recommendation: 'Schedule more practice time for coding exercises',
      reason: 'Based on your performance on recent programming assignments'
    },
    {
      course: 'Biology',
      recommendation: 'Try spaced repetition for memorizing terminology',
      reason: 'Your quiz scores indicate difficulty with terminology retention'
    }
  ];
}

// Function to detect academic risk factors
function detectAcademicRiskFactors() {
  // In a real implementation, this would analyze course data, attendance,
  // submission times, etc. to identify potential academic risks
  
  // Mock risk factors for demonstration
  return [
    {
      factor: 'Late submissions',
      course: 'Mathematics',
      recommendation: 'Set earlier personal deadlines for assignments'
    },
    {
      factor: 'Dropping attendance',
      course: 'Psychology',
      recommendation: 'Schedule fixed study times for reviewing lecture materials'
    }
  ];
}

// Function to integrate with UF systems (simulated)
function simulateUFIntegration() {
  // In a real implementation, this would connect to UF's systems
  // through approved APIs or data-sharing agreements
  
  // For the prototype, we're simulating this integration
  const academicData = {
    courses: [
      { id: 'COP3502', name: 'Programming Fundamentals 1', credits: 4, grade: 'A' },
      { id: 'MAC2311', name: 'Calculus 1', credits: 4, grade: 'B+' },
      { id: 'CHM2045', name: 'Chemistry 1', credits: 3, grade: 'A-' }
    ],
    gpa: 3.8,
    academicStanding: 'Good',
    advisorInfo: {
      name: 'Dr. Johnson',
      email: 'johnson@ufl.edu',
      office: 'CSE E432',
      hours: 'Mon/Wed 2-4pm'
    }
  };
  
  return academicData;
}

// Function to check if the user is verified as a UF student
function checkUFVerification() {
  // In a real implementation, this would check against a database
  // or UF's authentication system
  
  // For the prototype, we're simulating this verification
  const isVerified = localStorage.getItem('uf_verified') === 'true';
  return isVerified;
}

// Function to update the UF verification status
function setUFVerification(status) {
  localStorage.setItem('uf_verified', status);
  const badge = document.querySelector('.security-badge');
  if (badge) {
    badge.style.display = status ? 'inline-flex' : 'none';
  }
} 