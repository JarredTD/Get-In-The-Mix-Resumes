$(document).ready(function () {
  // Initialize the event handlers when the document is ready
  initModalEvents();
  initResumeHandlers();
});

/**
 * Initializes event handlers for the resume modal.
 */
function initModalEvents() {
  $("#resumeModal").on("show.bs.modal", loadResumeList);
}

/**
 * Loads resume list and binds event handlers to UI elements inside the modal.
 */
function loadResumeList() {
  $.ajax({
    url: "resumes/load-resume-ids",
    type: "GET",
    success: populateResumeList,
    error: function (xhr) {
      console.log("Error:", xhr.responseText);
    },
  });
}

/**
 * Populates the list of resumes in the UI.
 * @param {Array} response - List of resumes from the server.
 */
function populateResumeList(response) {
  const list = $("#resumeList");
  list.empty();
  response.forEach(function (resume) {
    const listItem = $(
      `<li>` +
        `Resume ID: <a href="#" class="load-resume" data-id="${resume.id}">${resume.id}</a> ` +
        `<button class='btn btn-success export-btn' data-id='${resume.id}'>Export</button> ` +
        `<button class='btn btn-danger delete-btn' data-id='${resume.id}'>Delete</button>` +
        `</li>`,
    );
    list.append(listItem);
  });
  bindButtonEvents();
}

/**
 * Binds click events for loading, exporting, and deleting resumes.
 */
function bindButtonEvents() {
  $(".load-resume").click(function (e) {
    e.preventDefault();
    loadResumeData($(this).data("id"));
    $("#resumeModal").modal("hide");
  });

  $(".export-btn").click(function () {
    window.location.href = `resumes/export-resume/${$(this).data("id")}`;
  });

  $(".delete-btn").click(function () {
    const id = $(this).data("id");
    if (confirm("Are you sure you want to delete this resume?")) {
      deleteResume(id);
    }
  });
}

/**
 * Sends a DELETE request to remove a resume.
 * @param {string} id - The ID of the resume to delete.
 */
function deleteResume(id) {
  $.ajax({
    url: `resumes/delete-resume/${id}`,
    type: "DELETE",
    success: function () {
      alert("Resume deleted successfully");
      $("#resumeModal").modal("hide");
      $("#resumeModal").modal("show");
    },
    error: function (xhr) {
      alert("Error deleting resume: " + xhr.responseText);
    },
  });
}

/**
 * Fetches and displays data for a specific resume.
 * @param {string} resumeId - ID of the resume to load.
 */
function loadResumeData(resumeId) {
  $.ajax({
    url: `resumes/load-resume/${resumeId}`,
    type: "GET",
    success: displayResumeData,
    error: function (xhr) {
      console.log("Error loading resume:", xhr.responseText);
    },
  });
}

/**
 * Displays the fetched resume data in the modal.
 * @param {Object} data - Data of the resume to display.
 */
function displayResumeData(data) {
  const infoContainer = $("#infoDisplay");
  infoContainer.empty();
  appendResumeData(data, infoContainer);
}

/**
 * Appends formatted resume data to a given element, ignoring empty entries and ids.
 * @param {Object} data - Resume data to append.
 * @param {jQuery} parentElement - The element to append data to.
 */
function appendResumeData(data, parentElement) {
  /**
   * Recursively appends data to the DOM, handling objects and arrays properly.
   * Ignores empty values and keys containing 'id'.
   * @param {string} key - The key for the current data item.
   * @param {*} value - The value for the current data item.
   * @param {jQuery} container - The container element to append data to.
   */
  function appendData(key, value, container) {
    if (!key.toLowerCase().includes("id") && value != null && value !== "") {
      const formattedKey = key.charAt(0).toUpperCase() + key.slice(1);
      if (Array.isArray(value) && value.length > 0) {
        const listContainer = $('<div class="mb-3">')
          .append(`<strong>${formattedKey}:</strong><ul class="list-unstyled">`)
          .appendTo(container);
        value.forEach((item) => {
          if (item) {
            const itemElement = $("<li>").appendTo(listContainer.find("ul"));
            if (typeof item === "object" && item !== null) {
              appendObjectData(item, itemElement);
            } else {
              itemElement.text(item);
            }
          }
        });
      } else if (
        typeof value === "object" &&
        value !== null &&
        Object.keys(value).length > 0
      ) {
        const objectContainer = $('<div class="mb-3">')
          .append(`<strong>${formattedKey}:</strong>`)
          .appendTo(container);
        Object.entries(value).forEach(([subKey, subValue]) => {
          appendData(
            subKey,
            subValue,
            $('<div class="pl-3">').appendTo(objectContainer),
          );
        });
      } else if (typeof value === "string" || typeof value === "number") {
        container.append(
          `<div><strong>${formattedKey}:</strong> ${value}</div>`,
        );
      }
    }
  }

  /**
   * Handles appending object data by delegating to appendData for each entry.
   * @param {Object} obj - The object whose entries will be appended.
   * @param {jQuery} container - The container element to append object entries to.
   */
  function appendObjectData(obj, container) {
    Object.entries(obj).forEach(([subKey, subValue]) => {
      appendData(subKey, subValue, container);
    });
  }

  Object.entries(data).forEach(([key, value]) => {
    appendData(key, value, parentElement);
  });
}
