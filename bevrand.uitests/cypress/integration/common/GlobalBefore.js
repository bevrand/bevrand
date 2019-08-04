before(() => {
    cy.request({
        url: 'http://localhost:4550/api/v1/private/testuser'
        }).then((response) => {
            let playlists = response.body['result'];
            playlists.forEach(function(playlist) {
                cy.request('DELETE', `http://localhost:4550/api/v1/private/testuser/${playlist.list}`)
        });
    });

    cy.request('http://localhost:4570/api/Users').then((response) => {
        let users = response.body['allUsers'];
        users.forEach(function(user) {
            cy.request('DELETE', `http://localhost:4570/api/Users?id=${user.id}`)
        });
    });

    cy.fixture('standarduser.json')
        .then((credentials) => {
        cy
            .request('POST', 'http://localhost:4570/api/Users', {
                'username': credentials.username,
                'emailAddress': credentials.emailAddress,
                'password': credentials.password
            })
            .then((response) => {
                // response.body is automatically serialized into JSON
                expect(response.body).to.have.property('username', credentials.username)
            })
    });

    cy.fixture('sampleplaylist.json')
        .then((playlist) => {
            cy
                .request('POST', `http://localhost:4550/api/v1/private/${playlist.username}/${playlist.playlistName}`, {
                    "beverages": playlist.beverages,
                    "displayName": playlist.displayName,
                    "imageUrl": playlist.imageUrl
                })
        });
});
