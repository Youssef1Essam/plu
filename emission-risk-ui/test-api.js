// Quick API test script
// Run with: node test-api.js

import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

async function testAPI() {
  console.log('🧪 Testing Industrial Emission Risk Monitor API\n');

  // Test 1: Health Check
  try {
    console.log('1️⃣ Testing health check...');
    const health = await axios.get(`${API_BASE_URL}/`);
    console.log('✅ Health check passed');
    console.log(`   Version: ${health.data.version}`);
    console.log(`   Status: ${health.data.status}\n`);
  } catch (error) {
    console.log('❌ Health check failed:', error.message);
    console.log('   Make sure backend is running on http://localhost:8000\n');
    return;
  }

  // Test 2: Scenario-based prediction
  try {
    console.log('2️⃣ Testing scenario-based prediction...');
    const scenarioData = {
      scenario: 'power_plant',
      location_type: 'urban'
    };
    const scenarioResult = await axios.post(`${API_BASE_URL}/predict-scenario`, scenarioData);
    console.log('✅ Scenario prediction passed');
    console.log(`   Risk Level: ${scenarioResult.data.risk_level}`);
    console.log(`   Impact Distance: ${scenarioResult.data.impact_distance_meters.toFixed(0)} m`);
    console.log(`   Confidence: ${(scenarioResult.data.confidence * 100).toFixed(0)}%\n`);
  } catch (error) {
    console.log('❌ Scenario prediction failed:', error.response?.data || error.message, '\n');
  }

  // Test 3: Custom prediction
  try {
    console.log('3️⃣ Testing custom prediction...');
    const customData = {
      emission_rate: 50,
      wind_speed: 3,
      stack_height: 100,
      exit_velocity: 15,
      stack_diameter: 3,
      stack_temperature: 400,
      ambient_temperature: 293,
      stability_class: 'D',
      location_type: 'industrial'
    };
    const customResult = await axios.post(`${API_BASE_URL}/predict`, customData);
    console.log('✅ Custom prediction passed');
    console.log(`   Risk Level: ${customResult.data.risk_level}`);
    console.log(`   Peak Concentration: ${customResult.data.peak_concentration.toExponential(2)} µg/m³`);
    console.log(`   Warnings: ${customResult.data.warnings.length} warning(s)\n`);
  } catch (error) {
    console.log('❌ Custom prediction failed:', error.response?.data || error.message, '\n');
  }

  console.log('✨ API testing complete!\n');
}

testAPI();
