"""E2b — Kiểm chứng vét cạn bổ sung với nhiều seed hơn ở 2000 và 5000 iteration (c = 1.4, rollout ngẫu nhiên)."""
from multiprocessing import Pool

from common import save, NPROC
from exp2_never_lose import verify

if __name__ == "__main__":
    jobs = [(it, 1.4, sd, side, "random") for it in (5000, 2000) for sd in range(100, 120) for side in (0, 1)]
    with Pool(NPROC) as pool:
        res = pool.map(verify, jobs, chunksize=1)
    save("e2b_never_lose_more.json", res)
    for it in (2000, 5000):
        rs = [r for r in res if r["it"] == it]
        print(it, "policies", len(rs), "lines", sum(r["lines"] for r in rs), "loss", sum(r["loss"] for r in rs),
              "opt", sum(r["optimal"] for r in rs), "/", sum(r["decisions"] for r in rs))
