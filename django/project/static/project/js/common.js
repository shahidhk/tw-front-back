"use strict";

function editProject(n) {
  var form, i;
  form = document.getElementById("project-details");
  for (i = 0; i < form.length; i++) {
    form[i].disabled = false;
  }
}

function saveProject(n) {
  var form;
  form = document.getElementById("project-details");
  Intercooler.triggerRequest(form);
}

function addPhase(n) {
  var form;
  var check = setInterval(function () {
    console.log('checking')
    if ($("#constructor_organization_name").length) {
      form = document.getElementById("phases-form");
      form.scrollIntoView();
      editPhase(n);
      clearInterval(check)
    }
  }, 100);
}

function editPhase(n) {
  var form, i;
  form = document.getElementById("phases-form");
  for (i = 0; i < form.length; i++) {
    form[i].disabled = false;
  }
}

function savePhase(n) {
  var form, i, button;
  form = document.getElementById("phases-form");
  Intercooler.triggerRequest(form);
}

function hidePhase(n) {
  document.getElementById("form-holder").attributes.style.value =
    "visibility:hidden";
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

function unHideForm(n) {
  document.getElementById("form-holder").attributes.style.value =
    "visibility: visible;";
}

$(function () {
  $(document).bind("error.ic", function (evt, elt, status, str, xhr) {
    alert(str);
  });
  $(document).bind("beforeSend.ic", function () {
    $.blockUI();
  });
  $(document).bind("complete.ic", function () {
    $.unblockUI();
  });
  $("#form-holder").on("success.ic", function (
    evt,
    elt,
    data,
    textStatus,
    xhr,
    requestId
  ) {
    document.getElementById("form-holder").attributes.style.value =
      "visibility:hidden";
  });
});