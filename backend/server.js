import express from "express";

const app = express();
app.use(express.json());

// Test route to verify server is working
app.get("/api/test", (req, res) => {
    res.json({ status: "Server is running" });
});

// Route to handle AQI data (frontend will call this)
app.post("/api/aqi", async (req, res) => {
    try {
        console.log("Received data:", req.body); // Debug log
        const { city, aqi } = req.body;
        if (typeof city !== "string" || typeof aqi !== "number") {
            return res.status(400).json({ error: "Invalid payload" });
        }
        // Just acknowledge receipt without storing
        console.log("Successfully processed:", { city, aqi }); // Debug log
        res.status(200).json({ message: "Data received successfully!" });
    } catch (err) {
        console.error(err);
        res.status(500).json({ error: "Failed to process data" });
    }
});

const PORT = 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
