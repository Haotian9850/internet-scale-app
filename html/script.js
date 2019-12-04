let history = [
    {
        "name": "samoyed",
        "views": 123,
    },
    {
        "name": "golden retriever",
        "views": 123
    },
    {
        "name": "lab",
        "views": 123
    }
];


function findMatch(keyword, history){
    return history.filter(entry => {
        if (entry.name.includes(keyword)){
            return keyword;
        }
    })
}


function displayMatches(){
    const matchedEntries = findMatch(this.value, history);
    console.log("matchedEntries", matchedEntries);
    const html = matchedEntries.map(entry => {
        //highlight matching search phrase
        const regex = new RegExp(this.value, 'gi');
        const name = entry.name.replace(regex, `<span class="h1">${this.value}</span>`);
        return `
            <li>
                <a href="#">
                <span class="name">${name}</span>
                <span class="population">${entry.views}</span>
                </a>
            </li>
        `;
    }).join('');
    suggestions.innerHTML = html;
}

const searchInput = document.querySelector('.searchBar');
const suggestions = document.querySelector('.suggestions');

searchInput.addEventListener('change', displayMatches);
searchInput.addEventListener('keyup', displayMatches);  







