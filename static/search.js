const searchBox = document.getElementById("companySearch");
const market = document.getElementById("market");
const suggestions = document.getElementById("suggestions");
const hiddenSymbol = document.getElementById("symbol");

searchBox.addEventListener("input", async function () {

    const keyword = searchBox.value.trim();

    if (keyword.length < 2) {
        suggestions.innerHTML = "";
        suggestions.style.display = "none";
        return;
    }

    const response = await fetch(
        `/search-stock?q=${keyword}&market=${market.value}`
    );

    const stocks = await response.json();

    suggestions.innerHTML = "";
    suggestions.style.display = "block";

    stocks.forEach(stock => {

        const item = document.createElement("div");

        item.className = "suggestion-item";

        item.innerHTML = `
            <div class="company-name">
                ${stock.name}
                <span class="company-exchange">
                    ${stock.exchange}
                </span>
            </div>

            <div class="company-symbol">
                ${stock.symbol}
            </div>
        `;

        item.onclick = function () {

            searchBox.value = stock.name;
            hiddenSymbol.value = stock.symbol;

            suggestions.innerHTML = "";
            suggestions.style.display = "none";

        };

        suggestions.appendChild(item);

    });

});