document.addEventListener("DOMContentLoaded", () => {
    // Tab switching logic
    const tabBtns = document.querySelectorAll(".tab-btn");
    const sections = document.querySelectorAll(".model-section");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active classes
            tabBtns.forEach(b => b.classList.remove("active"));
            sections.forEach(s => s.classList.remove("active"));
            
            // Hide all results when switching
            document.querySelectorAll(".result-card").forEach(r => r.classList.add("hidden"));

            // Add active class to clicked
            btn.classList.add("active");
            const targetId = btn.getAttribute("data-target");
            document.getElementById(targetId).classList.add("active");
        });
    });

    // Handle Tennis form submission
    const tennisForm = document.getElementById("tennis-form");
    tennisForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const btn = tennisForm.querySelector("button");
        const originalText = btn.innerHTML;
        btn.innerHTML = "Predicting...";
        btn.disabled = true;

        const payload = {
            outlook: document.getElementById("outlook").value,
            temp: document.getElementById("temp").value,
            humidity: document.getElementById("humidity").value,
            wind: document.getElementById("wind").value
        };

        try {
            const response = await fetch("/api/predict_tennis", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            const resultCard = document.getElementById("tennis-result");
            const resultText = document.getElementById("tennis-output");
            
            if (data.status === "Success") {
                resultText.textContent = data.prediction;
                resultCard.classList.remove("hidden");
            } else {
                resultText.textContent = "Error: " + data.error;
                resultCard.classList.remove("hidden");
            }
        } catch (err) {
            console.error(err);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });

    // Handle Social form submission
    const socialForm = document.getElementById("social-form");
    socialForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const btn = socialForm.querySelector("button");
        const originalText = btn.innerHTML;
        btn.innerHTML = "Predicting...";
        btn.disabled = true;

        const payload = {
            age: document.getElementById("age").value,
            salary: document.getElementById("salary").value,
            scaler_choice: document.getElementById("scaler_choice").value
        };

        try {
            const response = await fetch("/api/predict_social", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            const resultCard = document.getElementById("social-result");
            const resultText = document.getElementById("social-output");
            const scalerOut = document.getElementById("social-scaler-out");

            if (data.status === "Success") {
                resultText.textContent = data.prediction;
                scalerOut.textContent = "Used: " + (data.scaler_used === "standard" ? "Standard Scaler" : "MinMax Scaler");
                resultCard.classList.remove("hidden");
            } else {
                resultText.textContent = "Error: " + data.error;
                scalerOut.textContent = "";
                resultCard.classList.remove("hidden");
            }
        } catch (err) {
            console.error(err);
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    });
});
