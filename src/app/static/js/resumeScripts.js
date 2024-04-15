$(document).ready(function () {
  // Show the model
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

  // Function to load individual resume data
  function loadResumeData(resumeId) {
    $.ajax({
      url: `/load-resume/${resumeId}`,
      type: "GET",
      success: function (data) {
        populateFormFields(data);
      },
      error: function (xhr) {
        console.log("Error loading resume:", xhr.responseText);
      },
    });
  }

  // Function to populate form fields, including handling nested data structures
  function populateFormFields(data) {
    Object.entries(data).forEach(([key, value]) => {
      if (!Array.isArray(value)) {
        $(`#${key}`).val(value);
      }
    });

    populateNestedFields("experiences", data.experiences);
    populateNestedFields("educations", data.educations);
    populateNestedFields("projects", data.projects);
    populateNestedFields("skills", data.skills);
    populateNestedFields("courses", data.courses);
  }

  // Function to handle array-type nested data
  function populateNestedFields(containerId, items) {
    const container = $(`#${containerId}`);
    container.empty();

    if (items) {
      items.forEach((item, index) => {
        const formGroup = $('<div class="form-group">').appendTo(container);
        Object.entries(item).forEach(([key, value]) => {
          const label = $("<label>").text(
            key.charAt(0).toUpperCase() + key.slice(1) + ":",
          );
          let input;

          if (key.includes("bullet_points")) {
            input = $("<textarea>")
              .addClass("form-control")
              .attr("name", `${containerId}-${index}-${key}`);
          } else {
            input = $("<input>")
              .addClass("form-control")
              .attr("type", "text")
              .attr("name", `${containerId}-${index}-${key}`);
          }
          input.val(value);

          formGroup.append(label, input);
        });
      });
    }
  }
});
