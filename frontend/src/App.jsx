import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import './App.css';

const TOKEN = "demo"; // Using demo token - replace with your activated token later
const BACKEND_URL = "http://localhost:5000";

const getAqiStatus = (aqi) => {
    if (aqi > 300) return { status: 'Hazardous', color: '#e74c3c', bgClass: 'bg-hazardous' };
    if (aqi > 200) return { status: 'Very Unhealthy', color: '#e67e22', bgClass: 'bg-very-unhealthy' };
    if (aqi > 150) return { status: 'Unhealthy', color: '#f1c40f', bgClass: 'bg-unhealthy' };
    if (aqi > 100) return { status: 'Unhealthy for Sensitive Groups', color: '#f39c12', bgClass: 'bg-unhealthy-sensitive' };
    if (aqi > 50) return { status: 'Moderate', color: '#2ecc71', bgClass: 'bg-moderate' };
    return { status: 'Good', color: '#27ae60', bgClass: 'bg-good' };
};

const getHealthPrecautions = (aqi) => {
    if (aqi > 200) {
        return [
            "Everyone should avoid outdoor activities.",
            "Sensitive individuals should wear a mask outdoors.",
            "Keep windows closed and use an air purifier.",
            "Limit physical exertion even indoors."
        ];
    }
    if (aqi > 100) {
        return [
            "Outdoor activities are generally safe.",
            "Sensitive individuals should limit prolonged outdoor exertion.",
            "Consider wearing a mask if you're sensitive.",
            "Keep windows closed during peak hours."
        ];
    }
    return [
        "Enjoy your outdoor activities.",
        "No health concerns.",
        "Ideal conditions for most people."
    ];
};

const getPollutionSources = (city) => {
    const lowerCaseCity = city.toLowerCase();

    // Use a switch statement for cleaner city-specific logic
    switch (true) {
        case lowerCaseCity.includes('mumbai'):
            return [
                { name: 'Vehicle Emissions', value: 40, color: '#28a745' },
                { name: 'Construction', value: 25, color: '#e67e22' },
                { name: 'Industrial Activity', value: 20, color: '#007bff' },
                { name: 'Biomass Burning', value: 10, color: '#dc3545' },
                { name: 'Other', value: 5, color: '#6c757d' },
            ];
        case lowerCaseCity.includes('delhi'):
            return [
                { name: 'Vehicle Emissions', value: 35, color: '#28a745' },
                { name: 'Industrial Activity', value: 28, color: '#007bff' },
                { name: 'Power Generation', value: 18, color: '#ffc107' },
                { name: 'Biomass Burning', value: 12, color: '#dc3545' },
                { name: 'Other', value: 7, color: '#6c757d' },
            ];
        case lowerCaseCity.includes('bangalore'):
        case lowerCaseCity.includes('bengaluru'):
            return [
                { name: 'Vehicle Emissions', value: 30, color: '#28a745' },
                { name: 'Construction', value: 20, color: '#e67e22' },
                { name: 'Industrial Activity', value: 15, color: '#007bff' },
                { name: 'Waste Burning', value: 10, color: '#dc3545' },
                { name: 'Other', value: 25, color: '#6c757d' },
            ];
        // Add more cities here as needed
        // case lowerCaseCity.includes('london'):
        //     return [
        //         { name: 'Traffic', value: 45, color: '#28a745' },
        //         { name: 'Residential Heating', value: 30, color: '#e67e22' },
        //         { name: 'Other', value: 25, color: '#6c757d' },
        //     ];

        default:
            // This is the default data for any city not listed above
            return [
                { name: 'General Sources', value: 50, color: '#28a745' },
                { name: 'Other', value: 50, color: '#6c757d' },
            ];
    }
};

const getPollutantDescription = (name) => {
    switch (name) {
        case 'PM2.5':
            return 'Fine particulate matter. Can penetrate deep into the lungs.';
        case 'NO₂':
            return 'Nitrogen Dioxide. Primarily from vehicle exhaust and power plants.';
        case 'CO':
            return 'Carbon Monoxide. A poisonous gas from incomplete combustion.';
        case 'SO₂':
            return 'Sulfur Dioxide. A respiratory irritant from burning fossil fuels.';
        case 'O₃':
            return 'Ground-level Ozone. Harmful to lungs and a key component of smog.';
        case 'PM10':
            return 'Coarse particulate matter. Can cause respiratory issues.';
        default:
            return '';
    }
};

const getSourceDescription = (sourceName) => {
    switch (sourceName) {
        case 'Vehicle Emissions':
            return "This source refers to pollutants released from cars, trucks, and buses. It is a major contributor to urban smog and fine particulate matter.";
        case 'Industrial Activity':
            return "Pollution from factories, manufacturing plants, and other industrial processes. This can include a wide range of chemicals and particulates.";
        case 'Power Generation':
            return "Emissions from power plants, especially those that burn fossil fuels like coal, are a significant source of sulfur dioxide and nitrogen oxides.";
        case 'Biomass Burning':
            return "This includes pollutants from the burning of organic matter, such as wildfires, agricultural clearing, or residential wood stoves.";
        case 'Construction':
            return "Dust and particles from construction sites.";
        case 'Waste Burning':
            return "Burning of waste and trash in open areas.";
        case 'General Sources':
            return "A combination of common pollution sources for cities not in the database.";
        case 'Other':
            return "A combination of minor sources, including dust from construction sites, wind-blown soil, and natural events.";
        default:
            return "Information on this source is limited.";
    }
};

const AQIGauge = ({ aqi, color }) => {
    const radius = 45;
    const circumference = 2 * Math.PI * radius;
    const progress = Math.min(aqi / 300, 1);
    const dashoffset = circumference * (1 - progress);

    return (
        <div className="aqi-gauge-container">
            <svg viewBox="0 0 100 60" className="gauge-svg">
                <path
                    className="gauge-bg"
                    d="M5 50 A 45 45 0 0 1 95 50"
                />
                <path
                    className="gauge-arc"
                    d="M5 50 A 45 45 0 0 1 95 50"
                    stroke={color}
                    style={{
                        strokeDasharray: circumference,
                        strokeDashoffset: dashoffset
                    }}
                />
            </svg>
            <div className="aqi-gauge-value">{aqi}</div>
        </div>
    );
};

const PollutantCard = ({ name, value, safeLimit, trend, unit }) => {
    const percentage = Math.round((value / safeLimit) * 100);
    const description = getPollutantDescription(name);
    
    return (
        <div className="pollutant-card">
            <div className="pollutant-header">
                <span className="pollutant-name">{name}</span>
                <span className="pollutant-trend" style={{ color: trend >= 0 ? '#28a745' : '#dc3545' }}>
                    {trend >= 0 ? '▲' : '▼'} {Math.abs(trend)}%
                </span>
            </div>
            <div className="pollutant-value">{value} {unit}</div>
            <div className="safe-limit">Safe limit: {safeLimit} {unit}</div>
            <div className="progress-bar-container">
                <div
                    className="progress-bar"
                    style={{ width: `${Math.min(percentage, 100)}%`, backgroundColor: getAqiStatus(percentage).color }}
                ></div>
            </div>
            <div className="tooltip">{description}</div>
        </div>
    );
};

const AirQuality = () => {
    const [aqData, setAqData] = useState(null);
    const [mlResult, setMlResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [city, setCity] = useState("");
    const [inputCity, setInputCity] = useState("");
    const [error, setError] = useState("");
    const [healthPrecautions, setHealthPrecautions] = useState([]);
    const [pollutionSources, setPollutionSources] = useState([]);

    const fetchAQData = async (cityName) => {
        setLoading(true);
        setError("");
        setAqData(null);
        setMlResult(null);
        
        try {
            console.log("Fetching air quality data for:", cityName);
            
            // First, try to get data from WAQI API directly
            const response = await axios.get(
                `https://api.waqi.info/feed/${cityName}/?token=${TOKEN}`,
                { timeout: 10000 }
            );

            console.log("WAQI API Response:", response.data);

            if (response.data.status === "error" && response.data.data === "Invalid key") {
                setError("⚠️ API Token is invalid! Please:\n1. Get a new token from https://aqicn.org/data-platform/token/\n2. Update the TOKEN in App.jsx\n3. Restart the frontend");
                setHealthPrecautions([]);
                setPollutionSources([]);
                return;
            }

            if (response.data.status === "ok") {
                const data = response.data.data;
                setAqData(data);
                setCity(cityName);

                const iaqi = data.iaqi || {};
                const co = iaqi.co?.v || 0;
                const no2 = iaqi.no2?.v || 0;
                const pm25 = iaqi.pm25?.v || 0;
                const so2 = iaqi.so2?.v || 0;

                console.log("Pollutant values:", { CO: co, NO2: no2, "PM2.5": pm25, SO2: so2 });
                console.log("Sending to backend:", { CO: co, NO2: no2, "PM2.5": pm25, SO2: so2, city_name: cityName });
                
                const mlResponse = await axios.post(BACKEND_URL + '/predict', {
                    CO: co,
                    NO2: no2,
                    "PM2.5": pm25,
                    SO2: so2,
                    city_name: cityName
                }, {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    timeout: 10000
                });
                
                console.log("Backend response:", mlResponse.data);
                setMlResult(mlResponse.data);
                
                const aqi = mlResponse.data.aqi;
                
                setHealthPrecautions(getHealthPrecautions(aqi));
                setPollutionSources(getPollutionSources(cityName));

            } else {
                console.error("WAQI API returned non-ok status:", response.data);
                setError(`Unable to find air quality data for "${cityName}". Try: Delhi, Mumbai, London, or New York.`);
                setHealthPrecautions([]);
                setPollutionSources([]);
            }
        } catch (err) {
            console.error("Error fetching data:", err);
            
            let errorMessage = "";
            
            if (err.code === 'ECONNABORTED' || err.message.includes('timeout')) {
                errorMessage = "Request timed out. The air quality API might be slow or unavailable.";
            } else if (err.response) {
                // Server responded with error
                console.error("Server error:", err.response.data);
                
                if (err.response.status === 404) {
                    errorMessage = `City "${cityName}" not found. Try these cities: Delhi, Mumbai, London, New York, Tokyo, Paris`;
                } else if (err.response.status === 401 || err.response.status === 403) {
                    errorMessage = "API token is invalid or expired. Please check the TOKEN in App.jsx";
                } else if (err.response.status === 429) {
                    errorMessage = "API rate limit exceeded. Please wait a few minutes before trying again.";
                } else {
                    errorMessage = `Server error: ${err.response.data.error || err.response.statusText}`;
                }
            } else if (err.request) {
                // Request made but no response
                console.error("No response from server:", err.request);
                
                // Check which endpoint failed
                if (err.config?.url?.includes('waqi.info')) {
                    errorMessage = "Cannot connect to air quality API. Please check your internet connection.";
                } else {
                    errorMessage = "Cannot connect to backend server. Make sure Flask is running on port 5000.";
                }
            } else {
                // Something else happened
                console.error("Request error:", err.message);
                errorMessage = `Error: ${err.message}`;
            }
            
            setError(errorMessage);
            setHealthPrecautions([]);
            setPollutionSources([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (!city) {
            fetchAQData("Delhi");
        }
    }, [city]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputCity.trim() !== "") {
            fetchAQData(inputCity.trim());
            setInputCity("");
        }
    };

    const aqiValue = mlResult ? mlResult.aqi : 0;
    const aqiStatus = getAqiStatus(aqiValue);
    const now = new Date();

    const currentPollutionSource = pollutionSources[0] || {};
    const sourceDescription = getSourceDescription(currentPollutionSource.name);


    return (
        <div className={`app-container ${aqiStatus.bgClass}`}>
            <div className="title-container">
                <h1 className="main-title">Air Quality Monitor</h1>
                <p className="subtitle">Real-time air quality monitoring and health recommendations for your area</p>
            </div>

            <form onSubmit={handleSubmit} className="input-form">
                <input
                    type="text"
                    value={inputCity}
                    onChange={(e) => setInputCity(e.target.value)}
                    placeholder="Enter city (e.g. Delhi, London)"
                    className="city-input"
                />
                <button type="submit" className="check-button">
                    Check
                </button>
            </form>
            
            <div className="status-message">
                {loading && <div className="spinner"></div>}
                {error && <p className="error-message">🚨 {error}</p>}
            </div>

            {aqData && (
                <>
                    <div className="dashboard-grid">
                        <div className="card">
                            <h3 className="card-title">Air Quality Index for {city}</h3>
                            <div className="aqi-card-content">
                                <AQIGauge aqi={aqiValue} color={aqiStatus.color} />
                                <div className="aqi-status" style={{ backgroundColor: aqiStatus.color }}>
                                    {aqiStatus.status}
                                </div>
                                <p className="aqi-subtext">
                                    {aqiStatus.status === 'Good' ? 'Enjoy your outdoor activities.' : 'Limit outdoor exertion.'}
                                </p>
                                <p className="last-updated">Last updated: {now.toLocaleDateString()} {now.toLocaleTimeString()}</p>
                            </div>
                        </div>

                        <div className="pollutant-cards-grid">
                            <PollutantCard name="PM2.5" value={aqData.iaqi?.pm25?.v ?? 0} safeLimit={35} unit="µg/m³" trend={2.1} />
                            <PollutantCard name="NO₂" value={aqData.iaqi?.no2?.v ?? 0} safeLimit={100} unit="µg/m³" trend={-1.8} />
                            <PollutantCard name="CO" value={aqData.iaqi?.co?.v ?? 0} safeLimit={9} unit="µg/m³" trend={-0.5} />
                            <PollutantCard name="SO₂" value={aqData.iaqi?.so2?.v ?? 0} safeLimit={75} unit="µg/m³" trend={3.5} />
                            <PollutantCard name="O₃" value={aqData.iaqi?.o3?.v ?? 0} safeLimit={70} unit="µg/m³" trend={-0.2} />
                            <PollutantCard name="PM10" value={aqData.iaqi?.pm10?.v ?? 0} safeLimit={150} unit="µg/m³" trend={-0.8} />
                        </div>
                    </div>

                    <div className="dashboard-grid">
                        <div className="health-precautions-card">
                            <div className="health-status-header">
                                <span className="health-status-text">Health Precautions: <span style={{ color: aqiStatus.color }}>{aqiStatus.status}</span></span>
                            </div>
                            <ul className="health-precautions-list">
                                {healthPrecautions.map((precaution, index) => (
                                    <li key={index} className="precaution-item">
                                        <span role="img" aria-label="check-mark" style={{ color: aqiStatus.color, marginRight: '10px' }}>✅</span> {precaution}
                                    </li>
                                ))}
                            </ul>
                        </div>
                       <div className="card pollution-sources-card">
  <h3 className="card-title">Pollution Sources in {city}</h3>

  {pollutionSources.map((source, index) => (
    <div key={index} className="source-item">
      <div className="source-header">
        <span className="source-name">{source.name}</span>
        <span className="source-percentage">{source.value}%</span>
      </div>
      <div className="source-bar-container">
        <div
          className="source-bar"
          style={{
            width: `${source.value}%`,
            backgroundColor: source.color
          }}
        ></div>
      </div>
      <p className="source-description">{getSourceDescription(source.name)}</p>
    </div>
  ))}
</div>


                    </div>
                </>
            )}
        </div>
    );
};

export default AirQuality;