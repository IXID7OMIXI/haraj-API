let currentPage = 1;
let currentTag = "";
let isLoading = false;

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchBtn').addEventListener('click', () => doSearch(true));
    document.getElementById('loadMoreBtn').addEventListener('click', () => doSearch(false));
});

async function doSearch(isNewSearch) {
    if (isLoading) return;
    
    const tagInput = document.getElementById('tagInput').value;
    const gear = document.querySelector('input[name="gear"]:checked').value;
    const keywordsVal = document.getElementById('keywordsInput').value;
    const keywords = keywordsVal ? keywordsVal.split(',').map(s => s.trim()).filter(s => s) : [];

    if (isNewSearch) {
        currentPage = 1;
        document.getElementById('resultsGrid').innerHTML = '';
        currentTag = tagInput;
        document.getElementById('loadMoreBtn').classList.add('hidden');
    }

    setLoading(true);
    updateStatus(`Fetching page ${currentPage}...`);

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tag: currentTag,
                page: currentPage,
                limit: 20,
                gear_filter: gear || null,
                keywords: keywords
            })
        });

        if (!response.ok) throw new Error('Network response was not ok');
        
        const data = await response.json();
        renderResults(data.items);
        
        if (data.items.length > 0) {
            currentPage++;
            document.getElementById('loadMoreBtn').classList.remove('hidden');
            updateStatus(`Found ${data.items.length} items`);
        } else {
            if (isNewSearch) {
                updateStatus("No results found.");
            } else {
                updateStatus("No more results.");
                document.getElementById('loadMoreBtn').classList.add('hidden');
            }
        }

    } catch (error) {
        console.error('Error:', error);
        updateStatus("Error fetching data.");
    } finally {
        setLoading(false);
    }
}

function renderResults(items) {
    const grid = document.getElementById('resultsGrid');
    
    items.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        
        const price = item.price && item.price.formattedPrice ? item.price.formattedPrice : 'On Call';
        const gear = item.carInfo && item.carInfo.gear ? item.carInfo.gear : getGearFromText(item.title + (item.bodyTEXT || ""));
        const city = item.city || item.geoCity || '';
        const year = item.carInfo && item.carInfo.model ? item.carInfo.model : '';

        // Safely access properties
        const title = item.title || "No Title";
        
        // Construct full URL
        let postUrl = item.URL || "#";
        if (postUrl !== "#" && !postUrl.startsWith('http')) {
             // Remove leading slash explicitly if needed, although simple concat usually works
             // but let's be safe:
             if (postUrl.startsWith('/')) postUrl = postUrl.substring(1);
             postUrl = "https://haraj.com.sa/" + postUrl;
        }
        
        // Determine Image URL
        let imgUrl = "";

        // specific priority: check imagesList first for a full URL
        if (item.imagesList && item.imagesList.length > 0) {
             imgUrl = item.imagesList[0];
        }

        // Fallback to thumbURL if needed
        if (!imgUrl && item.thumbURL) {
            imgUrl = item.thumbURL;
            if (!imgUrl.startsWith('http')) {
                // Heuristic for Haraj CDN if path is relative
                imgUrl = "https://mimg6cdn.haraj.com.sa/userfiles30/" + imgUrl;
            }
        }
        
        // HTML for Image area
        let imgHTML = '';
        if (imgUrl) {
            // Ensure no broken images if empty string
            imgHTML = `<img src="${imgUrl}" alt="${title}" loading="lazy" style="width:100%; height:100%; object-fit:cover; border-radius: 8px 8px 0 0;">`;
        } else {
            imgHTML = `
                <div class="card-img-placeholder">
                    <span>No Image</span>
                </div>`;
        }
        
        card.innerHTML = `
            <a href="${postUrl}" target="_blank" style="text-decoration:none; color:inherit; height:100%; display:flex; flex-direction:column;">
                <div style="height: 200px; width: 100%; position: relative; background-color: #2c2c2e;">
                    ${imgHTML}
                </div>
                <div class="card-body">
                    <h3 dir="auto">${title}</h3>
                    <div class="tags">
                        ${year} ${gear ? `• ${gear}` : ''}
                    </div>
                    <div class="card-meta">
                        <span>${city}</span>
                        <span class="price">${price}</span>
                    </div>
                </div>
            </a>
        `;
        grid.appendChild(card);
    });
}

function getGearFromText(text) {
    if (!text) return "";
    if (text.includes("عادي") || text.toLowerCase().includes("manual")) return "Manual";
    if (text.includes("توماتيك") || text.toLowerCase().includes("auto")) return "Auto";
    return "";
}

function setLoading(loading) {
    isLoading = loading;
    const btn = document.getElementById('searchBtn');
    btn.textContent = loading ? "Loading..." : "Search";
    btn.disabled = loading;
}

function updateStatus(msg) {
    document.getElementById('status').textContent = msg;
}
