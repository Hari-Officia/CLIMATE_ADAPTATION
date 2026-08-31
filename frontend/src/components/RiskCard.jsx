export default function RiskCard({ hazard, data }) {
  const color = data.risk === 'HIGH' ? 'bg-red-500' : 'bg-green-500';
  return (
    <div className="border p-4 rounded shadow">
      <h2 className="font-bold text-xl">{hazard}</h2>
      <p>Prob: {data.probability.toFixed(2)}</p>
      <div className={`text-white px-2 mt-2 inline-block rounded ${color}`}>{data.risk}</div>
    </div>
  );
}
