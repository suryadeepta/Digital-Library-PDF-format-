// Custom file input logic
const realFileBtn = document.getElementById("real-file");
const customBtn = document.getElementById("custom-button");
const fileName = document.getElementById("file-name");

customBtn.addEventListener("click", () => {
  realFileBtn.click();
});

realFileBtn.addEventListener("change", () => {
  fileName.textContent = realFileBtn.files.length > 0 
    ? realFileBtn.files[0].name 
    : "No file chosen";
});

// Background changer
const bgSelector = document.getElementById("bgSelector");
const customBgInput = document.getElementById("customBgInput");

const backgrounds = {
  1: "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa",
  2: "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
  3: "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f",
  4: "https://images.unsplash.com/photo-1501785888041-af3ef285b470"
};

function setBackground(url) {
  document.body.style.backgroundImage = `url('${url}')`;
  localStorage.setItem("customBg", url);
}

bgSelector.addEventListener("change", () => {
  if (bgSelector.value === "custom") {
    customBgInput.style.display = "block";
  } else {
    customBgInput.style.display = "none";
    setBackground(backgrounds[bgSelector.value]);
  }
});

customBgInput.addEventListener("input", () => {
  const url = customBgInput.value.trim();
  if (url.length > 5) {
    setBackground(url);
  }
});

// Load background from local storage if available
const savedBg = localStorage.getItem("customBg");
if (savedBg) {
  setBackground(savedBg);
  // Find if this matches any of our predefined backgrounds
  const matchingKey = Object.keys(backgrounds).find(
    key => backgrounds[key] === savedBg
  );
  if (matchingKey) {
    bgSelector.value = matchingKey;
  } else {
    bgSelector.value = "custom";
    customBgInput.style.display = "block";
    customBgInput.value = savedBg;
  }
}