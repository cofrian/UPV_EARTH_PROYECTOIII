"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const BAR_COLORS = [
  "#37a374",
  "#e9b44c",
  "#5aa9e6",
  "#f9844a",
  "#90be6d",
  "#c77dff",
  "#43aa8b",
  "#f94144",
  "#577590",
  "#f3722c",
];

const PIE_COLORS = [
  "#00a896",
  "#f4a261",
  "#4ea8de",
  "#f94144",
  "#90be6d",
  "#9b5de5",
  "#2a9d8f",
  "#e76f51",
  "#577590",
  "#e9c46a",
];

const AXIS_TICK = { fill: "#d9efe5", fontSize: 11 };
const GRID_STROKE = "#2a4538";
const TOOLTIP_STYLE = {
  backgroundColor: "#0f1c17",
  borderColor: "#335a4a",
  color: "#d9efe5",
};

const BarChartAny = BarChart as any;
const LineChartAny = LineChart as any;
const PieChartAny = PieChart as any;
const CartesianGridAny = CartesianGrid as any;
const XAxisAny = XAxis as any;
const YAxisAny = YAxis as any;
const TooltipAny = Tooltip as any;
const BarAny = Bar as any;
const LineAny = Line as any;
const PieAny = Pie as any;
const CellAny = Cell as any;
const LegendAny = Legend as any;

type Pair = {
  label: string;
  value: number;
};

type KeywordPair = {
  keyword: string;
  value: number;
};

function hasData(data: Pair[]): boolean {
  return data.length > 0 && data.some((item) => item.value > 0);
}

function shortLabel(label: string, max = 18): string {
  if (!label) return "";
  if (label.length <= max) return label;
  return `${label.slice(0, max - 1)}...`;
}

export function DistBarChart({ data }: { data: Pair[] }) {
  if (!hasData(data)) {
    return <div className="h-72 w-full grid place-items-center muted">No hay datos para mostrar</div>;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <BarChartAny data={data} margin={{ top: 10, right: 12, left: 0, bottom: 48 }}>
          <CartesianGridAny strokeDasharray="3 3" stroke={GRID_STROKE} />
          <XAxisAny
            dataKey="label"
            angle={-30}
            textAnchor="end"
            interval={0}
            tick={AXIS_TICK}
            minTickGap={8}
            tickFormatter={(value: string) => shortLabel(value)}
          />
          <YAxisAny tick={AXIS_TICK} width={42} />
          <TooltipAny
            contentStyle={TOOLTIP_STYLE}
            labelStyle={{ color: "#d9efe5" }}
            formatter={(value: number, _name: string, entry: { payload?: Pair }) => [value, entry?.payload?.label || "valor"]}
          />
          <BarAny dataKey="value" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <CellAny key={`${entry.label}-${index}`} fill={BAR_COLORS[index % BAR_COLORS.length]} />
            ))}
          </BarAny>
        </BarChartAny>
      </ResponsiveContainer>
    </div>
  );
}

export function DistLineChart({ data }: { data: Pair[] }) {
  if (!hasData(data)) {
    return <div className="h-72 w-full grid place-items-center muted">No hay datos para mostrar</div>;
  }

  const isYearSeries = data.every((item) => /^\d{4}$/.test(item.label));
  const xTickInterval = isYearSeries ? Math.max(0, Math.ceil(data.length / 12) - 1) : "preserveStartEnd";
  const showDots = data.length <= 24;

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <LineChartAny data={data} margin={{ top: 10, right: 12, left: 0, bottom: isYearSeries ? 40 : 24 }}>
          <CartesianGridAny strokeDasharray="3 3" stroke={GRID_STROKE} />
          <XAxisAny
            dataKey="label"
            tick={AXIS_TICK}
            interval={xTickInterval}
            angle={isYearSeries ? -30 : 0}
            textAnchor={isYearSeries ? "end" : "middle"}
            minTickGap={isYearSeries ? 10 : 8}
            tickFormatter={(value: string) => shortLabel(value, 10)}
          />
          <YAxisAny tick={AXIS_TICK} width={42} />
          <TooltipAny contentStyle={TOOLTIP_STYLE} labelStyle={{ color: "#d9efe5" }} />
          <LineAny
            type="monotone"
            dataKey="value"
            stroke="#f2c14e"
            strokeWidth={3}
            dot={showDots ? { r: 2.5, fill: "#f2c14e" } : false}
            activeDot={{ r: 4, fill: "#f2c14e" }}
          />
        </LineChartAny>
      </ResponsiveContainer>
    </div>
  );
}

export function DistPieChart({ data }: { data: Pair[] }) {
  if (!hasData(data)) {
    return <div className="h-72 w-full grid place-items-center muted">No hay datos para mostrar</div>;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer>
        <PieChartAny>
          <TooltipAny contentStyle={TOOLTIP_STYLE} labelStyle={{ color: "#d9efe5" }} />
          <LegendAny
            wrapperStyle={{ fontSize: 12, color: "#d9efe5" }}
            formatter={(value: string) => shortLabel(value, 22)}
          />
          <PieAny
            data={data}
            dataKey="value"
            nameKey="label"
            innerRadius={52}
            outerRadius={94}
            paddingAngle={2}
            minAngle={2}
          >
            {data.map((entry, index) => (
              <CellAny key={`${entry.label}-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
            ))}
          </PieAny>
        </PieChartAny>
      </ResponsiveContainer>
    </div>
  );
}

export function KeywordBars({ data }: { data: KeywordPair[] }) {
  const chartData = data.map((item) => ({ label: item.keyword, value: item.value }));
  return <DistBarChart data={chartData} />;
}

export function LengthComparisonChart({
  paperLength,
  globalAvg,
  pbAvg,
}: {
  paperLength: number;
  globalAvg: number;
  pbAvg: number;
}) {
  const data = [
    { label: "Paper", value: paperLength },
    { label: "Media global", value: Math.round(globalAvg) },
    { label: "Media mismo PB", value: Math.round(pbAvg) },
  ];
  return <DistBarChart data={data} />;
}
