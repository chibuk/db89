{
  let addOption = (id, value, text) => {    /* id - parent tag, value - attribute, text - InnerHTML */
    let elem = document.getElementById(id);
    let newOpt = document.createElement('option');
    newOpt.innerHTML = text;
    newOpt.value = value;
    elem.appendChild(newOpt);
  }
    let url = 'http://127.0.0.1:8000/api/v1/organizations/';
    fetch(url)
  .then(response => response.json())
  .then(commits => {
    document.getElementById("id_sender").replaceChildren();
    document.getElementById("id_receiver").replaceChildren();
    addOption('id_sender', "-1", "-----");
    let receiver1Tag = document.getElementById("id_receiver1");
    receiver1Tag.setAttribute('list', 'receiver-list');
    let newDatalist = document.createElement('datalist');
    newDatalist.setAttribute('id', 'receiver-list');
    receiver1Tag.appendChild(newDatalist);
    document.getElementById("id_payer").replaceChildren();
    for (let i in commits) {
        addOption('id_sender', commits[i].id, commits[i].name);
        addOption('id_receiver', commits[i].id, commits[i].name);
        addOption('id_payer', commits[i].id, commits[i].name);
        addOption('receiver-list', commits[i].name, commits[i].inn);
    }
  })
}
