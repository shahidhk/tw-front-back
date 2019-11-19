"use strict";

function addRow(n) {
  var table = document.getElementById("tbl");
  var row = table.insertRow(-1);
  var cell;
  row.className = "data";
  cell = row.insertCell(0);
  cell.innerText = "Auto Generated";
  for (var i = 1; i < 4; i++) {
    cell = row.insertCell(i);
    cell.innerHTML = '<input type="text">';
  }
  cell = row.insertCell(i);
  cell.innerHTML =
    '<img src="/static/project/save-2.svg" alt="Save Phase Entry" onclick="savePhase(this);">';
}

function editProject(n) {
  var form, i;
  n.innerText = "Save Project";
  n.setAttribute("onclick", "saveProject(this);");
  form = document.getElementById("project-details");
  for (i = 0; i < form.length; i++) {
    form[i].disabled = false;
  }
}

function saveProject(n) {
  var form, i, button;
  n.innerText = "Edit Project";
  n.setAttribute("onclick", "editProject(this);");
  form = document.getElementById("project-details");
  Intercooler.triggerRequest(form, function(data) {
    updateProject(data);
  });
  for (i = 0; i < form.length; i++) {
    form[i].disabled = true;
  }
  // button = document.querySelector("form div button");
  // button.click()
  // form.submit();
}

function editPhase(n) {
  var cell, row, i, cellText;
  row = n.parentNode.parentNode;
  for (i = 1; i < 4; i++) {
    cell = row.children[i];
    cellText = cell.innerText;
    cell.innerHTML =
      '<input type="text" id="' +
      cell.firstChild.id +
      '" value="' +
      cellText +
      '">';
  }
  cell = row.children[i];
  // this will be the last cell
  cell.innerHTML =
    '<input type="image" src="/static/project/save-2.svg" alt="Save Phase" onclick="savePhase(this);">';
}

function savePhase(n) {
  var data = {},
    row = n.parentNode.parentNode;
  const Url = "http://" + document.location.host + "/api/save-phase/";
  data["phase_id"] = row.id;
  for (i = 1; i < 4; i++) {
    cell = row.children[i];
    data[cell.firstChild.id] = cell.firstChild.value;
  }
  var axiosConfig = {
    headers: {
      "X-CSRFToken": Cookies.get("csrftoken")
    }
  };
  axios
    .post(Url, data, axiosConfig)
    .then(function(response) {
      updatePhase(response);
    })
    .catch(function(error) {
      console.log(error);
    });
  console.log(Url + " with cookie " + Cookies.get("csrftoken"));
  console.log(data);
}

function updatePhase(n) {
  console.log(n);
  var row = document.getElementById(n.data.phase_id);
  var colID = ["name", "number", "description"];
  var cell = row.children[0];
  cell.innerHTML = '<a href="google.com">' + n.data.phase_id + "</a>";
  for (i = 1; i < 4; i++) {
    cell = row.children[i];
    cell.innerHTML =
      '<a id="' +
      colID[i - 1] +
      '" href="google.com">' +
      n.data[colID[i - 1]] +
      "</a>";
  }
  cell = row.children[i];
  // this will be the last cell
  cell.innerHTML =
    '<input type="image" src="/static/project/edit-5.svg" alt="Edit Phase" onclick="editPhase(this);">';
}

function updateProject(n) {
  console.log(n);
  var form = document.getElementById("project-details");
  var data = JSON.parse(n);
  for (const [key, value] of Object.entries(data)) {
    console.log(key, value);
  }
  // TODO actually put the values into the form
}

function editRole(n) {
  var userForm, row, cell, i;
  userForm = document.getElementById("project-role");
  userForm.attributes.style.value = "visibility:visible";
  row = n.parentNode.parentNode;
  userForm.children[2].children[0].value = row.children[0].innerText;
  for (i = 0; i < 3; i++) {
    cell = row.children[i];
    userForm.children[i + 3].children[1].value = cell.innerText;
  }
  cell = row.children[i];
  // this will be the last cell
  cell.innerHTML =
    '<input type="image" src="/static/project/x-mark-7.svg" alt="Cancel Editing Role" onclick="stopEditRole(this);">';
}

function stopEditRole(n) {
  document.getElementById("project-role").attributes.style.value =
    "visibility: hidden;";
  n.parentElement.innerHTML =
    '<input type="image" src="/static/project/edit-5.svg" alt="Edit My Role" onclick="editRole(this);">';
}

function constructionPhaseDetails(n) {
  document.getElementById("form-holder").attributes.style.value =
    "visibility: visible;";
}

$(function() {
  $("#project-role").on("error.ic", function(evt, elt, status, str, xhr) {
    console.log(str);
  });
  $("#project-role").on("complete.ic", function(
    evt,
    elt,
    data,
    status,
    xhr,
    requestId
  ) {
    document.getElementById("project-role").attributes.style.value =
      "visibility:hidden";
  });
});
