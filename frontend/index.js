// fetch shelter data
async function getShelterData() {
    const URL = "/api/shelters";
    const container = document.getElementById("shelter-card-container");

    try {
        const response = await fetch(URL);
        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status}`);
        }
        const data = await response.json();
        keys = Object.keys(data);
        keys.forEach(key => {
            createArticlesHolders(data[key], container);
            const card = document.createElement("div");
            card.classList.add("card-container");
            const cardContent = `
                <h2>${post.title}</h2>
                <p>${post.body}</p>
            `;
            card.innerHTML = cardContent;
            container.appendChild(card);
        });
    } catch (error) {
        console.error(`Error fetching data:`, error);
        container.innerHTML = `<p>Failed to load data. Please try again later.</p>`
    }
}

getShelterData();

// fetch pets data and display html
async function getPetsData() {
    const apiKey = "live_H422Hok8pHFRCPvVxN7imW5EIvJN16DPS6W65fOUjBlgEz45L3vcOe8MaWU9uaZP"
    const URL = `wss://api.thedogapi.com=${apiKey}`;
    const container = document.getElementById("pets-card-container");

    try {
        const response = await fetch(URL);
        if (!response.ok) {
            throw new Error(`Error! Status: ${response.status}`);
        }
        const data = await response.json();
        keys = Object.keys(data);
        keys.forEach(key => {
            createArticlesHolders(data[key], container);
            const card = document.createElement("div");
            card.classList.add("card-container");
            const cardContent = `
                <h2>${post.title}</h2>
                <p>${post.body}</p>
            `;
            card.innerHTML = cardContent;
            container.appendChild(card);
        });
    } catch (error) {
        console.error(`Error fetching data:`, error);
        container.innerHTML = `<p>Failed to load data. Please try again later.</p>`
    }
}
getPetsData();