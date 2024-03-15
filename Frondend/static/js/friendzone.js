document.addEventListener('DOMContentLoaded', function() {
    fetch('/user/')
    .then(response => response.text())
    .then(data => {
        document.getElementById('userName').innerText = data;
    });
});


document.addEventListener('DOMContentLoaded', function () {
    // Event-Listener für den Button "anschauen" hinzufügen
    var anschauenButtons = document.querySelectorAll('.anschauen');
    anschauenButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            zeigeMitglieder();
        });
    });
});

// Funktion zum Abrufen aller Freundeszonen
// Annahme: Der folgende Code wird in einem Webbrowser oder einer ähnlichen Umgebung ausgeführt

// Ersetze 'ID_HIER_EINFÜGEN' durch die tatsächliche ID, die du abrufen möchtest
const fzId = 1;

// Erstellen der URL für die GET-Anfrage
const url = `/api/friendzone/${fzId}`;

// Ausführen einer GET-Anfrage an die API
fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Ausgabe aller Friendzonen in der Konsole
        console.log(data);
        // Anzahl der Elemente dynamisch setzen
        const numElements = data.length;
        // Schleife über alle Elemente
        for (let i = 0; i < numElements; i++) {
            const element = data[i];
            // Den Wert "data" in die "card-title" setzen
            document.getElementsByClassName('card-title')[i].innerText = element.data;
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });



        // // Fügen Sie diese Funktion hinzu, um den Benutzernamen zu aktualisieren
        // function updateUsername() {
        //     $.ajax({
        //         url: "/user/", // URL für die Backend-Funktion zum Abrufen des Benutzernamens
        //         type: "GET",
        //         success: function (response) {
        //             var usernameLink = document.getElementById('usernameLink');
        //             usernameLink.innerHTML = response.username;
        //         },
        //         error: function (xhr, status, error) {
        //             console.error(error);
        //             // Fehlerbehandlung hier einfügen
        //         }
        //     });
        // }

        // Rufen Sie die Funktion bei Bedarf auf, z. B. beim Laden der Seite
        // updateUsername();


        // Funktion, um Gruppen dynamisch zu laden
        $(document).ready(function () {
            // AJAX-Anfrage an den Server senden, um die Gruppen abzurufen
            $.ajax({
                url: "/api/friendzone/", // URL für die Backend-Funktion zum Abrufen der Gruppen
                type: "GET",
                success: function (response) {
                    var gruppen = JSON.parse(response);
                    var gruppenListe = document.getElementById('gruppenListe');

                    gruppen.forEach(function (gruppe) {
                        var listItem = document.createElement('li');
                        var link = document.createElement('a');

                        link.href = "#";
                        link.onclick = function () { zeigeMitglieder(gruppe.id); };
                        link.textContent = gruppe.name;

                        listItem.appendChild(link);
                        gruppenListe.appendChild(listItem);
                    });
                },
                error: function (xhr, status, error) {
                    console.error(error);
                    // Fehlerbehandlung hier einfügen
                }
            });
        });

        // Funktion, um Mitglieder zu einer Gruppe anzuzeigen
        function zeigeMitglieder(gruppenName) {
            // Hier müsste die Funktionalität implementiert werden, um die Mitglieder aus der Datenbank abzurufen
            // und sie dann der Liste im Popup-Fenster hinzuzufügen

            // AJAX-Anfrage an den Server senden, um Benutzerdaten abzurufen
            $.ajax({
                url: "/api/get_all_users", // URL für die Backend-Funktion zum Abrufen aller Benutzer
                type: "GET",
                success: function (response) {
                    var users = JSON.parse(response);
                    var mitgliederListe = document.getElementById('mitgliederListe');
                    mitgliederListe.innerHTML = ""; // Vorhandene Liste löschen

                    users.forEach(function (user) {
                        var listItem = document.createElement('tr');
                        var td1 = document.createElement('td');
                        var td2 = document.createElement('td');
                        var deleteButton = document.createElement('button');

                        td1.className = 'title';
                        td2.className = 'action text-right';
                        deleteButton.className = 'btn btn-danger mt-4';

                        td1.innerHTML = `
                                                <div class="thumb">
                                                    <img class="img-fluid" src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="">
                                                </div>
                                                <div class="candidate-list-details">
                                                    <div class="candidate-list-info">
                                                        <div class="candidate-list-title">
                                                            <h5 class="mb-0"><a href="#">${user.first_name} ${user.last_name}</a></h5>
                                                        </div>
                                                    </div>
                                                </div>
                                            `;
                        deleteButton.innerHTML = '<i class="far fa-trash-alt"></i>';
                        deleteButton.onclick = function () {
                            listItem.remove();
                        };

                        td2.appendChild(deleteButton);
                        listItem.appendChild(td1);
                        listItem.appendChild(td2);
                        mitgliederListe.appendChild(listItem);
                    });

                    // Popup-Fenster anzeigen
                    document.getElementById('popup').style.display = 'block';
                    document.getElementById('overlay').style.display = 'block';
                },
                error: function (xhr, status, error) {
                    console.error(error);
                    // Fehlerbehandlung hier einfügen
                }
            });
        }


        // Funktion, um das Popup-Fenster zu schließen
        document.getElementById('overlay').onclick = function () {
            document.getElementById('popup').style.display = 'none';
            document.getElementById('overlay').style.display = 'none';
        };

        // Funktion, um das Formular für ein neues Mitglied anzuzeigen
        function zeigeNeuesMitgliedForm() {
            document.getElementById('popup').style.display = 'none';
            document.getElementById('neuesMitgliedForm').style.display = 'block';
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('groupElements').style.display = 'none';

        }

        // Funktion, um ein neues Mitglied hinzuzufügen
        function fuegeNeuesMitgliedHinzu() {
                var user_email = document.getElementById("neuesMitgliedName").value;
                var data = {
                    friendzone_id: 2,
                    user_email: user_email
                };
            
                fetch('/api/invite_fz/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
                alert("Email erfolgreich abgesendet!")
            
                document.getElementById('neuesMitgliedForm').style.display = 'none';
                document.getElementById('groupElements').style.display = 'block';

        //     document.getElementById('popup').style.display = 'none';
        //     var neuesMitgliedName = document.getElementById('neuesMitgliedName').value;
        //     var mitgliederListe = document.getElementById('mitgliederListe');
        //     var listItem = document.createElement('tr');
        //     var td1 = document.createElement('td');
        //     var td2 = document.createElement('td');
        //     var deleteButton = document.createElement('button');

        //     td1.className = 'title';
        //     td2.className = 'action text-right';
        //     deleteButton.className = 'btn btn-danger';

        //     td1.innerHTML = `
        //     <div class="thumb">
        //         <img class="img-fluid" src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="">
        //     </div>
        //     <div class="candidate-list-details">
        //         <div class="candidate-list-info">
        //             <div class="candidate-list-title">
        //                 <h5 class="mb-0"><a href="#">${neuesMitgliedName}</a></h5>
        //             </div>
        //         </div>
        //     </div>
        // `;
        //     deleteButton.innerHTML = '<i class="far fa-trash-alt"></i>';
        //     deleteButton.onclick = function () {
        //         listItem.remove();
        //     };

        //     td2.appendChild(deleteButton);
        //     listItem.appendChild(td1);
        //     listItem.appendChild(td2);
        //     mitgliederListe.appendChild(listItem);

        //     // Formular ausblenden, nachdem das neue Mitglied hinzugefügt wurde
        //     document.getElementById('neuesMitgliedForm').style.display = 'none';
        //      document.getElementById('popup').style.display = 'block';

        //     // Zusätzliche Logik zum Hinzufügen des neuen Mitglieds zur Datenbank kann hier implementiert werden
        }

// AJAX-Anfrage an den Server senden, um alle Benutzerdaten abzurufen
$(document).ready(function () {
    $.ajax({
        url: "/api/get_all_users", // URL für die Backend-Funktion zum Abrufen aller Benutzer
        type: "GET",
        success: function (response) {
            var users = JSON.parse(response);
            var vorschlaegeListe = document.getElementById('vorschlaege');

            // Iteriere durch Benutzer und füge ihre E-Mails als Optionen hinzu
            users.forEach(function (user) {
                var option = document.createElement('option');
                option.value = user.email;
                vorschlaegeListe.appendChild(option);
            });
        },
        error: function (xhr, status, error) {
            console.error(error);
            // Fehlerbehandlung hier einfügen
        }
    });
});

// Funktion zum Laden von Vorschlägen basierend auf dem eingegebenen Text
function ladeVorschlaege() {
    var inputText = document.getElementById('neuesMitgliedName').value.toLowerCase();
    var vorschlaege = document.getElementById('vorschlaege');

    // Lösche vorhandene Optionen
    vorschlaege.innerHTML = "";

    // Füge Optionen basierend auf dem eingegebenen Text hinzu
    var options = document.querySelectorAll('#vorschlaege option');
    options.forEach(function (option) {
        var optionValue = option.value.toLowerCase();
        if (optionValue.includes(inputText)) {
            vorschlaege.appendChild(option);
        }
    });
}