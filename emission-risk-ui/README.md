# Industrial Emission Risk Monitor - Frontend

A clean, modern React decision interface for the Industrial Emission Risk Monitor system.

## 🎯 Goal

Help users **understand emission risk in 3 seconds** through a visual, decision-focused interface.

## ✨ Features

### Two Input Modes

1. **Scenario Mode** (Default)
   - Pre-configured emission scenarios
   - Quick risk assessment
   - Options: Power Plant, Factory, Waste Incinerator

2. **Custom Mode**
   - Full control over all physics parameters
   - Advanced users can input exact values
   - All Gaussian plume model parameters

### Result Display

- **Large Risk Badge**: Instant visual feedback (LOW/MEDIUM/HIGH)
- **Key Metrics Grid**: Impact distance, width, time, peak location, concentration
- **AI Explanation**: Human-friendly analysis powered by Gemma 4
- **Recommendation**: Clear, actionable guidance
- **Warnings**: Automatic alerts for concerning conditions
- **Confidence Score**: Visual confidence indicator
- **Population Risk**: Special alerts for urban areas

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- Backend running on `http://localhost:8000`

### Installation

```bash
cd emission-risk-ui
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### Build for Production

```bash
npm run build
npm run preview
```

## 🏗️ Architecture

```
src/
├── components/
│   ├── InputSection.tsx          # Mode toggle + input forms
│   ├── ResultCard.tsx            # Main result container
│   ├── RiskBadge.tsx             # Large risk indicator
│   ├── MetricsGrid.tsx           # Key metrics display
│   ├── ExplanationSection.tsx    # AI explanation
│   ├── RecommendationBox.tsx     # Action recommendation
│   ├── WarningsList.tsx          # Warning alerts
│   ├── ConfidenceBar.tsx         # Confidence indicator
│   └── PopulationRiskBanner.tsx  # Population risk alert
├── services/
│   └── api.ts                    # API client (Axios)
├── App.tsx                       # Main application
├── App.css                       # Animations
└── index.css                     # Tailwind imports
```

## 🎨 Design Principles

1. **Minimal & Clean**: White background, clear spacing, no clutter
2. **Visual Hierarchy**: Risk badge dominates, metrics support
3. **Instant Understanding**: User sees risk level in <3 seconds
4. **Mobile Responsive**: Stacks beautifully on small screens
5. **Smooth Transitions**: Loading states and animations

## 📡 API Integration

### Endpoints Used

- `POST /predict-scenario` - Scenario-based analysis
- `POST /predict` - Custom parameter analysis

### Response Structure

```typescript
interface RiskAssessmentResponse {
  risk_level: string;
  peak_concentration: number;
  impact_distance_meters: number;
  effective_height: number;
  explanation: string;
  recommendation: string;
  confidence: number;
  warnings: string[];
  impact_width_meters?: number;
  time_to_impact_minutes?: number;
  peak_distance_meters?: number;
  population_risk?: string;
  uncertainty_range?: { min: number; max: number };
}
```

## 🧪 Testing

### Manual Testing Checklist

1. **Scenario Mode**
   - [ ] Select each scenario (Power Plant, Factory, Waste Burning)
   - [ ] Change location type (Industrial, Urban, Rural)
   - [ ] Click "Analyze Risk"
   - [ ] Verify result displays correctly

2. **Custom Mode**
   - [ ] Switch to Custom Mode
   - [ ] Enter custom values
   - [ ] Verify all inputs work
   - [ ] Submit and check result

3. **Result Display**
   - [ ] Risk badge shows correct color
   - [ ] All metrics display properly
   - [ ] Explanation is readable
   - [ ] Recommendation is clear
   - [ ] Warnings appear when present
   - [ ] Confidence bar animates

4. **Error Handling**
   - [ ] Backend offline → Error message
   - [ ] Invalid input → Validation
   - [ ] Network error → User-friendly message

5. **Responsive Design**
   - [ ] Desktop (1920px)
   - [ ] Tablet (768px)
   - [ ] Mobile (375px)

## 🔧 Configuration

### Backend URL

Edit `src/services/api.ts`:

```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### Proxy (Optional)

Vite proxy is configured in `vite.config.ts` for `/api` routes.

## 📦 Dependencies

### Core
- React 19.2.5
- TypeScript 6.0.2
- Vite 8.0.10

### UI
- TailwindCSS 4.2.4
- PostCSS 8.5.13
- Autoprefixer 10.5.0

### HTTP
- Axios 1.16.0

## 🎯 Success Criteria

✅ User understands risk in <3 seconds  
✅ Clear decision visible immediately  
✅ All backend fields displayed properly  
✅ Mobile responsive  
✅ Smooth loading states  
✅ Error handling  

## 📝 Notes

- This is a **DECISION INTERFACE**, not a dashboard
- No charts, no complex maps, no overdesign
- Focus on clarity and instant understanding
- Backend must be running on port 8000

## 🐛 Troubleshooting

### Frontend won't start
```bash
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend connection error
- Ensure backend is running: `python main.py`
- Check backend URL in `src/services/api.ts`
- Verify CORS is enabled on backend

### Build errors
```bash
npm run build
# Check for TypeScript errors
```

## 📄 License

Part of the Industrial Emission Risk Monitor system v2.2.0
