import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 50,
  duration: '1m',
  thresholds: {
    // 95th percentile of request duration must be < 50ms
    http_req_duration: ['p(95)<50'],
  },
};

export default function () {
  // Replace with your actual API endpoint for getting an item
  const url = __ENV.API_URL + '/items/test123';
  let res = http.get(url);
  check(res, {
    'status was 200': (r) => r.status === 200,
    'p95 < 50ms': (r) => r.timings.duration < 50,
  });
  sleep(1);
}
