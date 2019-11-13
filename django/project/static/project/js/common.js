function addRow(n) {
    var table = document.getElementById('tbl');
    var row = table.insertRow(-1);
    var cell;
    row.className = "data";
    cell = row.insertCell(0);
    cell.innerText = 'Auto Generated';
    for (var i = 1; i < 4; i++) {
        cell = row.insertCell(i);
        cell.innerHTML = '<input type="text">';
    };
    cell = row.insertCell(i);
    cell.innerHTML = '<img src="/static/project/save-2.svg" alt="Save Phase Entry" onclick="savePhase(this);">';
};

function editProject(n) {
    console.log(n);
    n.innerText = "Save Project";
};

function editPhase(n) {
    var cell, row, i, cellText;
    row = n.parentNode.parentNode;
    for (i = 1; i < 4; i++) {
        cell = row.children[i];
        cellText = cell.innerText;
        cell.innerHTML = '<input type="text" id="' + cell.firstChild.id + '" value="' + cellText + '">';
    };
    cell = row.children[i];
    // this will be the last cell
    cell.innerHTML = '<input type="image" src="/static/project/save-2.svg" alt="Save Phase" onclick="savePhase(this);">';
};

function savePhase(n) {
    var data = {}, row = n.parentNode.parentNode;
    const Url = 'http://' + document.location.host + '/api/save-phase/';
    data['phase_id'] = row.id;
    for (i = 1; i < 4; i++) {
        cell = row.children[i];
        data[cell.firstChild.id] = cell.firstChild.value;
    };
    var axiosConfig = {
        headers: {
            'X-CSRFToken': Cookies.get("csrftoken")
        }
    };
    // $.ajaxSetup({
    //     headers: {
    //         'X-CSRFToken': Cookies.get("csrftoken")
    //     }
    // });
    // $.post(Url, data, function (data, status) {
    //     console.log('data is ' + data + ' status is ' + status);
    // });
    axios.post(Url, data, axiosConfig)
        .then(function (response) {
            updatePhase(response)
        })
        .catch(function (error) {
            console.log(error);
        });
    console.log(Url + ' with cookie ' + Cookies.get("csrftoken"));
    console.log(data);
};

function updatePhase(n) {
    console.log(n);
    var row = document.getElementById(n.data.phase_id);
    var colID = ['name', 'number', 'description'];
    var cell = row.children[0];
    cell.innerHTML = '<a href="google.com">' + n.data.phase_id + '</a>'
    for (i = 1; i < 4; i++) {
        cell = row.children[i];
        cell.innerHTML = '<a id="' + colID[i - 1] + '" href="google.com">' + n.data[colID[i - 1]] + '</a>'
    };
    cell = row.children[i];
    // this will be the last cell
    cell.innerHTML = '<input type="image" src="/static/project/edit-5.svg" alt="Edit Phase" onclick="editPhase(this);">';
}