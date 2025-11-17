import { useRef } from 'react';

interface DeferredType {
  promise: (Promise<unknown>),
  resolve: ((value: unknown) => void),
  reject: ((reason?: unknown) => void),
}

export const makeDeferred = (): DeferredType  => {
  const deferred: Partial<DeferredType> = {
    promise: undefined,
    resolve: undefined,
    reject: undefined
  };

  deferred.promise = new Promise((resolve, reject) => {
    deferred.resolve = resolve;
    deferred.reject = reject;
  });
  return deferred as DeferredType;
}

const apiFetchGen = <T, J>(apiFetch: (value: T, init?: RequestInit) => Promise<J>) => {
  let prom: Promise<J> | null = null;
  let abort: AbortController | null = null;

  return (value: T): Promise<J> => {
    if (abort) {
      abort.abort();
    }

    abort = new AbortController();

    const {
      promise: nProm,
      resolve: nResolve,
      reject: nReject
    } = makeDeferred();

    const _prom = apiFetch(value, {
      signal: abort.signal,
    }).then((d) => {
      if (_prom === prom) {
        nResolve(d);
        return d;
      }
    }).catch(err=>{
      if (err?.name === "AbortError")
        return;

      nReject(err);
    });

    prom = _prom as Promise<J>;
    return nProm as Promise<J>;
  };
};

export const useApi = <T, J>(apiFetch: (params: T, init?: RequestInit) => Promise<J>) => {
  const _fetch = useRef(apiFetchGen(apiFetch));
  return _fetch.current;
};