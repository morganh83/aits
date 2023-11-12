var cloneCount = 0;
var line_count = 1;
var punish_count = 1;

var filter_id = {
    "punT1": true
};
var optionsCache = {};

var ticket_form = {
    "revive": {
        "1": {
            "username": '',
            "discordID": null,
            "steamID": null,
            "growth": null,
            "dino": '',
        }
    },
    "punish": {
        "1": {
            "username": '',
            "steamID": null,
            "discordID": null,
            "punishment": '',
            "banLength": '',
            "otherBanLength": '',
            "brokenRules": [],
            "reason": ''
        }
    },
    "ticketLink": '',
    "additionalMods": '',
    "counterLink": ''
}


function filterType(filter_btn) {
    tbody = $(filter_btn).closest('tbody').attr("id");
    if (filter_btn.checked) {
        filter_id[tbody] = false;
    }
    else {
        filter_id[tbody] = true;
    }
    input = filter_btn.parentNode.parentNode.parentNode.children[0]
    input.value = "";
    restoreOptions(filter_btn, 'switch');
}

function filterItems(el) {
    var value = el.value.toLowerCase();
    var opt, sel = el.parentNode.children[2];
    curr_id = $(el.parentNode.children[2]).closest('tbody').attr("id");
    filtered_id = filter_id[curr_id]
    if (value == '') {
        restoreOptions(el, 'filter');
    } else {
        for (var i = sel.options.length - 1; i >= 0; i--) {
            opt = sel.options[i];
            if (filtered_id) {
                if (opt.id.toLowerCase().indexOf(value) == -1) {
                    sel.removeChild(opt)
                }
            }
            else {
                if (opt.value.toLowerCase().indexOf(value) == -1) {
                    sel.removeChild(opt)
                }
            }
        }
    }
}

function restoreOptions(id, type) {
    if (type == "filter") {
        var sel = id.parentNode.children[2];
    }
    else {
        var sel = id.parentNode.parentNode.parentNode.children[2];
    }
    loaded_cache = $(sel).closest('tbody').attr("id");
    current_cache = optionsCache[loaded_cache];
    sel.options.length = 0;
    for (let i = 0; i < current_cache.length; i++) {
        sel.appendChild(current_cache[i]);
    }
}


window.onload = function () {
    var sel = document.getElementById('id_allRules');
    loaded_cache = $(sel).closest('tbody').attr("id");
    optionsCache[loaded_cache] = [];
    for (var i = 0, iLen = sel.options.length; i < iLen; i++) {
        optionsCache[loaded_cache].push(sel.options[i]);
    }
}

function addNewLine() {
    var cloneReviveRows = document.getElementById('template_rev').content.cloneNode(true);

    line_count += 1;
    cloneReviveRows.querySelector('#rev_table').id = 'rev_table' + line_count;
    ticket_form['revive'][line_count] = {
        "username": '',
        "steamID": null,
        "growth": null,
        "dino": '',
    }

    document.getElementById('reviveTable').appendChild(cloneReviveRows);
}

function remLine(id) {
    if (line_count > 1) {
        $(id).closest('tbody').remove();
        tr_id = $(id).closest('tbody').attr('id');
        tr_num = tr_id.substring(tr_id.length - 1);
        delete ticket_form['revive'][tr_num];
        line_count -= 1;
    }
};

function addNewPunishLine() {
    var clonePunishRows = document.getElementById('template_punish').content.cloneNode(true);

    punish_count += 1;
    clonePunishRows.querySelector('#punT').id = 'punT' + punish_count;
    ticket_form['punish'][punish_count] = {
        "username": '',
        "steamID": null,
        "discordID": null,
        "punishment": '',
        "banLength": '',
        "otherBanLength": '',
        "brokenRules": [],
        "reason": ''
    }

    sel = clonePunishRows.querySelector('#id_allRules');
    loaded_cache = 'punT' + punish_count;
    optionsCache[loaded_cache] = [];
    filter_id[loaded_cache] = true;
    for (var i = 0, iLen = sel.options.length; i < iLen; i++) {
        optionsCache[loaded_cache].push(sel.options[i]);
    }

    document.getElementById('punishTable').appendChild(clonePunishRows);
}

function rmLinePunish(id) {
    if (punish_count > 1) {
        $(id).closest('tbody').remove();
        tr_id = $(id).closest('tbody').attr('id');
        tr_num = tr_id.substring(tr_id.length - 1);
        delete ticket_form['punish'][tr_num];
        punish_count -= 1;
    }
}

function addRule(rule) {
    var opt = document.createElement('option');
    opt.id = rule.id;
    opt.innerHTML = rule.innerHTML;
    tbody = $(rule).closest('tbody').attr('id');
    tbody_num = tbody.substring(tbody.length - 1);
    brokenRules_arr = ticket_form['punish'][tbody_num]["brokenRules"]
    brokenRules_arr.push(opt.id);
    opt.onclick = function () {
        ruleIndex = brokenRules_arr.indexOf(opt.id);
        brokenRules_arr.splice(ruleIndex, 1)
        $(opt).parent().parent().parent().first().first().find('#' + opt.id).show();
        $(opt).remove();
    };
    children = $(rule).closest('.col-5').parent().children();
    $(children[2]).find("#id_selectedRules").append(opt);
    $(rule).hide();
    console.log(ticket_form['punish']);

}

function checkPropertiesNone(obj) {
    for (var key in obj) {
        if (obj[key] !== null && obj[key] != "")
            return false;
    }
    return true;
}

function submit(csrf) {

    revNum = document.getElementById('reviveTable').childElementCount;
    for (let i = 1; i <= revNum; i++) {

        let tr_id = "rev_table" + String(i);
        let dict_count = ticket_form['revive'][i]
        let null_loop = ["discordID", "steamID", "username", "growth", "dino"]

        dict_count["username"] = $("#" + tr_id).find("#id_revUsername").val();
        dict_count["discordID"] = $("#" + tr_id).find("#id_revDiscordID").val();
        dict_count["steamID"] = $("#" + tr_id).find("#id_revSteamid").val();
        dict_count["growth"] = $("#" + tr_id).find("#id_revgrowth").val();
        dict_count["dino"] = $("#" + tr_id).find("#id_revdinoName").val();

        no_properties = checkPropertiesNone(dict_count);
        if (no_properties) {
            delete ticket_form['revive'][i];
        }

        dict_count["revive"] = $("#" + tr_id).find("#id_revd").is(":checked");

        for (let j = 0; j < null_loop.length; j++) {
            if (dict_count[null_loop[j]] == "") {
                dict_count[null_loop[j]] = null;
            }
        };
    }

    punishNum = document.getElementById('punishTable').childElementCount;
    for (let i = 1; i <= punishNum; i++) {
        let tb_id = "punT" + String(i);
        let dict_count = ticket_form['punish'][i]
        let null_loop = ["discordID", "steamID", "username", "reason", "otherBanLength"]
        dict_count['username'] = $("#" + tb_id).find("#id_OffigName").val();
        dict_count['steamID'] = $("#" + tb_id).find("#id_Offsteamid").val();
        dict_count['discordID'] = $("#" + tb_id).find("#id_OffdiscName").val();
        dict_count['punishment'] = $("#" + tb_id).find("#id_Offpunishment").val();
        dict_count['banLength'] = $("#" + tb_id).find("#id_OffbanTime").val();
        dict_count['otherBanLength'] = $("#" + tb_id).find("#id_OffbanTimeOther").val();
        dict_count['reason'] = $("#" + tb_id).find("#id_Offreason").val();

        no_properties = checkPropertiesNone(dict_count);
        if (no_properties) {
            delete ticket_form['punish'][i];
        }

        for (let j = 0; j < null_loop.length; j++) {
            if (dict_count[null_loop[j]] == "") {
                dict_count[null_loop[j]] = null;
            }
        };

    }

    ticket_form['additionalMods'] = $("#id_baseaddtlMods").val();
    ticket_form['ticketLink'] = $("#id_baseticketLink").val();
    ticket_form['counterLink'] = $("#id_basecounterLink").val();

    send_ticket(csrf);
}

function send_ticket(csrf_token) {

    fetch(String(window.origin) + '/ticket_call/', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(ticket_form),
        cache: 'no-cache',
        headers: new Headers({
            'content-type': 'application/json',
            'X-CSRFToken': csrf_token
        })
    })
        .then((response) => {
            response.json().then((dataReply) => {
                if (dataReply['courtesies']) {
                    window.location.href = String(window.origin) + '/courtesy/' + dataReply['courtesies'] + '/0';
                }
                else {
                    window.location.href = String(window.origin) + '/courtesy/none/0';
                }
            });
        });
}

function steamIdGet(id, csrf) {

    tbody = $(id).closest('tbody');

    if ($(id).val()) {
        fetch(String(window.origin) + '/getPunishedInfo?' + new URLSearchParams({
            id: $(id).val(),
            csrfmiddlewaretoken: csrf
        }))
            .then((response) => {
                response.json().then((dataReply) => {
                    if ("error" in dataReply) {
                        $(tbody).find("#previous_table").hide();
                        $(tbody).find("#previous_text").show();
                        $(tbody).find("#previous_text").html('This Steam ID has no punishments');
                    }
                    else {
                        $(tbody).find("#previous_text").hide();
                        $(tbody).find("#previous_offences").empty();

                        $(tbody).find('#previous_count').html(`Previous Offenses: ${dataReply['punishCount']}`);

                        for (let i = 0; i < dataReply['users'].length; i++) {
                            let tr = document.createElement("tr");

                            let v1 = document.createElement("td");
                            let v1_text = document.createTextNode(dataReply['users'][i][0].substring(0, 10));
                            v1.appendChild(v1_text);
                            tr.appendChild(v1);

                            let v2 = document.createElement("td");
                            let v2_text = document.createTextNode(dataReply['users'][i][2]);
                            v2.appendChild(v2_text);
                            tr.appendChild(v2);

                            let v3 = document.createElement("td");
                            let v3_text = document.createTextNode('Discord ID:' + dataReply['users'][i][3]);
                            v3.appendChild(v3_text);
                            tr.appendChild(v3);

                            if (dataReply['users'][i][1][1]) {
                                let v4 = document.createElement("td");
                                let v4_a = document.createElement("a");
                                v4_a.href = dataReply['users'][i][1][0];
                                let v4_text = document.createTextNode('Ticket Link');
                                v4_a.appendChild(v4_text);
                                v4.appendChild(v4_a);
                                tr.appendChild(v4);
                            }
                            else {
                                console.log(dataReply['users'][i][1][1])
                                let v4 = document.createElement("td");
                                let v4_text = document.createTextNode(dataReply['users'][i][1][0]);
                                v4.appendChild(v4_text);
                                tr.appendChild(v4);
                            }

                            $(tbody).find("#previous_offences").append(tr);
                        }

                        $(tbody).find("#previous_table").show();
                    }
                });
            });
    }
    else {
        $(tbody).find("#previous_table").hide();
        $(tbody).find("#previous_text").show();
        $(tbody).find("#previous_text").html('Enter a Steam ID to check previous offenses');
    }
}