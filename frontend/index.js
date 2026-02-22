// fetch shelter data
async function fetchJson(endpoint) {
    const response = await fetch("/api/" + endpoint);
    if (!response.ok) {
        throw new Error(`Error! Status: ${response.status}`);
    }
    return response.json();
}

async function displayShelters() {
    try {
        const json = await fetchJson("shelters");
        const container = document.getElementById("shelter-card-container");
        for(let i = 0; i < json.length; i++) {
            let obj = json[i];

            //{name: 'cohort', email: 'ivory-orchid@cohort.org', phone: '+156547896542', address: '12 rue de Prony, 75017 Paris, France'}
            const content = `
                <div class="card" id="shelter-${obj.id}">
                    <div class="card-content">
                        <h3>${obj.name}</h3>
                        <p>Email: ${obj.email}</p>
                        <p>Phone: ${obj.phone}</p>
                        <p>Address: ${obj.address}</p>
                    </div>
                </div>
                <br />
            `;
            container.innerHTML += content;
            console.log(obj.id);
        }
    } catch (error) {
        console.error(`Error fetching data:`, error);
        document.getElementById("shelter-card-container").innerHTML = `<p>Failed to load data. Please try again later.</p>`
    }
}
