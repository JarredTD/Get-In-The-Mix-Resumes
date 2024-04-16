$(document).ready(function () {
  // Show the modal
  $("#resumeModal").on("show.bs.modal", function (e) {
    $.ajax({
      url: "/load-resume-ids",
      type: "GET",
      success: function (response) {
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
      },
      error: function (xhr) {
        console.log("Error:", xhr.responseText);
      },
    });
  });

  function bindButtonEvents() {
    $(".load-resume").click(function (e) {
      e.preventDefault();
      const id = $(this).data("id");
      loadResumeData(id);
      $("#resumeModal").modal("hide");
    });

    $(".export-btn").click(function () {
      const id = $(this).data("id");
      window.location.href = `/export-resume/${id}`;
    });

    $(".delete-btn").click(function () {
      const id = $(this).data("id");
      if (confirm("Are you sure you want to delete this resume?")) {
        $.ajax({
          url: `/delete-resume/${id}`,
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
    });
  }

  // Load individual resume data
  function loadResumeData(resumeId) {
    $.ajax({
      url: `/load-resume/${resumeId}`,
      type: "GET",
      success: function (data) {
        displayResumeData(data);
      },
      error: function (xhr) {
        console.log("Error loading resume:", xhr.responseText);
      },
    });
  }

  // Display formatted resume data
  function displayResumeData(data) {
    const infoContainer = $("#infoDisplay");
    infoContainer.empty();

    function appendData(key, value, parentElement) {
      const formattedKey = key.charAt(0).toUpperCase() + key.slice(1);
      if (Array.isArray(value)) {
        const listContainer = $('<div class="mb-3">').appendTo(parentElement);
        listContainer.append(
          `<strong>${formattedKey}:</strong><ul class="list-unstyled">`,
        );
        value.forEach((item, index) => {
          const itemElement = $("<li>").appendTo(listContainer.find("ul"));
          if (typeof item === "object" && item !== null) {
            appendObjectData(item, itemElement);
          } else {
            itemElement.text(item);
          }
        });
      } else if (typeof value === "object" && value !== null) {
        const objectContainer = $('<div class="mb-3">').appendTo(parentElement);
        objectContainer.append(`<strong>${formattedKey}:</strong>`);
        appendObjectData(value, objectContainer);
      } else {
        parentElement.append(
          `<div><strong>${formattedKey}:</strong> ${value}</div>`,
        );
      }
    }

    function appendObjectData(obj, container) {
      const objContainer = $('<ul class="list-unstyled pl-3">').appendTo(
        container,
      );
      Object.entries(obj).forEach(([subKey, subValue]) => {
        if (!subKey.toLowerCase().includes("id")) {
          const formattedSubKey =
            subKey.charAt(0).toUpperCase() + subKey.slice(1);
          if (typeof subValue !== "object") {
            objContainer.append(`<li>${formattedSubKey}: ${subValue}</li>`);
          } else {
            appendData(subKey, subValue, $("<li>").appendTo(objContainer));
          }
        }
      });
    }

    const generalInfoKeys = [
      "First_name",
      "Last_name",
      "Email",
      "Phone_number",
      "Github_link",
      "Linkedin_link",
      "Entry_date",
    ];
    const generalInfo = {};
    const detailedInfo = {};

    Object.keys(data).forEach((key) => {
      if (generalInfoKeys.includes(key)) {
        generalInfo[key] = data[key];
      } else {
        detailedInfo[key] = data[key];
      }
    });

    Object.entries(generalInfo).forEach(([key, value]) => {
      if (!key.toLowerCase().includes("id")) {
        appendData(key, value, infoContainer);
      }
    });

    Object.entries(detailedInfo).forEach(([key, value]) => {
      if (!key.toLowerCase().includes("id")) {
        appendData(key, value, infoContainer);
      }
    });
  }
});
