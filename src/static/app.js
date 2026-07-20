document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const actionsContent = document.getElementById("actions-content");
  let allActivities = {};
  let selectedActivity = null;
  let studentEmail = null;

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      allActivities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(allActivities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";
        activityCard.style.cursor = "pointer";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        // Add click handler to select activity
        activityCard.addEventListener("click", () => {
          window.scrollTo({ top: 0, behavior: "smooth" });
          selectActivity(name);
        });

        activitiesList.appendChild(activityCard);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Function to select an activity and update actions panel
  function selectActivity(activityName) {
    selectedActivity = activityName;
    const activity = allActivities[activityName];
    const isRegistered = studentEmail && activity.participants.includes(studentEmail);

    let actionsHTML = `<div class="details-panel">
        <div>
          <h4 style="color: #0066cc; margin-bottom: 8px;">${activityName}</h4>
          <p style="margin-bottom: 16px; color: #444;">${activity.description}</p>
        </div>
        <div class="detail-row">
          <span class="detail-label">Schedule</span>
          <span class="detail-value">${activity.schedule}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Availability</span>
          <span class="detail-value">${activity.max_participants - activity.participants.length} spots left</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Capacity</span>
          <span class="detail-value">${activity.participants.length}/${activity.max_participants}</span>
        </div>
        <div>
          <p class="detail-heading">Participants</p>
          <ul class="participants-list">
            ${activity.participants.length > 0 ? activity.participants.map(p => `<li>${p}</li>`).join('') : `<li>No participants yet</li>`}
          </ul>
        </div>
      </div>`;

    if (!studentEmail) {
      actionsHTML += `
        <div class="form-group">
          <label for="email">Student Email:</label>
          <input type="email" id="email" required placeholder="your-email@mergington.edu" />
        </div>
        <div class="form-group">
          <button id="signup-btn" type="button">Sign Up for Activity</button>
        </div>
        <div id="message" class="hidden"></div>
      `;
    } else if (isRegistered) {
      actionsHTML += `
        <p style="margin-bottom: 15px;"><strong>You are registered for this activity</strong></p>
        <div class="form-group">
          <button id="drop-btn" type="button">Drop Activity</button>
        </div>
        <div id="message" class="hidden"></div>
      `;
    } else {
      actionsHTML += `
        <p style="margin-bottom: 15px;">Your email: <strong>${studentEmail}</strong></p>
        <div class="form-group">
          <button id="signup-btn" type="button">Sign Up for Activity</button>
        </div>
        <div id="message" class="hidden"></div>
      `;
    }

    actionsContent.innerHTML = actionsHTML;

    // Attach event listeners
    const messageDiv = document.getElementById("message");
    const signupBtn = document.getElementById("signup-btn");
    const dropBtn = document.getElementById("drop-btn");
    const emailInput = document.getElementById("email");

    if (signupBtn) {
      signupBtn.addEventListener("click", async () => {
        const email = emailInput ? emailInput.value : studentEmail;

        if (!email) {
          messageDiv.textContent = "Please enter an email address";
          messageDiv.className = "error";
          messageDiv.classList.remove("hidden");
          return;
        }

        studentEmail = email;

        try {
          const response = await fetch(
            `/activities/${encodeURIComponent(selectedActivity)}/signup?email=${encodeURIComponent(email)}`,
            { method: "POST" }
          );

          const result = await response.json();

          if (response.ok) {
            messageDiv.textContent = result.message;
            messageDiv.className = "success";
            fetchActivities();
            setTimeout(() => selectActivity(selectedActivity), 500);
          } else {
            messageDiv.textContent = result.detail || "An error occurred";
            messageDiv.className = "error";
          }

          messageDiv.classList.remove("hidden");
          setTimeout(() => {
            messageDiv.classList.add("hidden");
          }, 5000);
        } catch (error) {
          messageDiv.textContent = "Failed to sign up. Please try again.";
          messageDiv.className = "error";
          messageDiv.classList.remove("hidden");
          console.error("Error signing up:", error);
        }
      });
    }

    if (dropBtn) {
      dropBtn.addEventListener("click", async () => {
        try {
          const response = await fetch(
            `/activities/${encodeURIComponent(selectedActivity)}/drop?email=${encodeURIComponent(studentEmail)}`,
            { method: "POST" }
          );

          const result = await response.json();

          if (response.ok) {
            messageDiv.textContent = result.message;
            messageDiv.className = "success";
            fetchActivities();
            setTimeout(() => selectActivity(selectedActivity), 500);
          } else {
            messageDiv.textContent = result.detail || "An error occurred";
            messageDiv.className = "error";
          }

          messageDiv.classList.remove("hidden");
          setTimeout(() => {
            messageDiv.classList.add("hidden");
          }, 5000);
        } catch (error) {
          messageDiv.textContent = "Failed to drop activity. Please try again.";
          messageDiv.className = "error";
          messageDiv.classList.remove("hidden");
          console.error("Error dropping activity:", error);
        }
      });
    }
  }

  // Initialize app
  fetchActivities();
});
