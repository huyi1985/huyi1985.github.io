---
title: code
date: '2026-03-06'
---

```rust
use std::time::Instant;
use std::collections::hash_map::RandomState;
use std::hash::{BuildHasher, Hasher};

fn sum_naive(numbers: &[f32]) -> (f32, f64) {
    let start = Instant::now();
    let mut sum32: f32 = 0.0;
    let mut sum64: f64 = 0.0;
    for &f in numbers {
        sum32 += f;
        sum64 += f as f64;
    }
    let elapsed = start.elapsed().as_secs_f64();
    println!("Sum (naive):     f32={sum32}  f64={sum64}");
    println!("Time:            {elapsed:.3} seconds");
    (sum32, sum64)
}

fn sum_sorted(numbers: &[f32]) -> (f32, f64) {
    let start = Instant::now();
    let mut sorted = numbers.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let mut sum32: f32 = 0.0;
    let mut sum64: f64 = 0.0;
    for &f in &sorted {
        sum32 += f;
        sum64 += f as f64;
    }
    let elapsed = start.elapsed().as_secs_f64();
    println!("Sum (sorted):    f32={sum32}  f64={sum64}");
    println!("Sort+sum time:   {elapsed:.3} seconds");
    (sum32, sum64)
}

fn sum_gauss(numbers: &[f32]) -> (f32, f64) {
    let start = Instant::now();
    let n = numbers.len();
    let mut sorted = numbers.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let mut sum32: f32 = 0.0;
    let mut sum64: f64 = 0.0;
    for i in 0..n / 2 {
        let pair32 = sorted[i] + sorted[n - 1 - i];
        sum32 += pair32;
        let pair64 = sorted[i] as f64 + sorted[n - 1 - i] as f64;
        sum64 += pair64;
    }
    if n % 2 == 1 {
        sum32 += sorted[n / 2];
        sum64 += sorted[n / 2] as f64;
    }
    let elapsed = start.elapsed().as_secs_f64();
    println!("Sum (Gauss):     f32={sum32}  f64={sum64}");
    println!("Gauss time:      {elapsed:.3} seconds");
    (sum32, sum64)
}

fn sum_random_pick(numbers: &[f32]) -> (f32, f64) {
    let start = Instant::now();
    let n = numbers.len();
    // Use a Vec<usize> as the "set" of remaining indices, swap-remove for O(1) removal
    let mut indices: Vec<usize> = (0..n).collect();
    let mut rng: u64 = RandomState::new().build_hasher().finish();
    let mut sum32: f32 = 0.0;
    let mut sum64: f64 = 0.0;
    while !indices.is_empty() {
        rng ^= rng << 13;
        rng ^= rng >> 7;
        rng ^= rng << 17;
        let pick = (rng as usize) % indices.len();
        let idx = indices.swap_remove(pick);
        sum32 += numbers[idx];
        sum64 += numbers[idx] as f64;
    }
    let elapsed = start.elapsed().as_secs_f64();
    println!("Sum (random_pick): f32={sum32}  f64={sum64}");
    println!("Random pick time: {elapsed:.3} seconds");
    (sum32, sum64)
}

fn sum_kahan(numbers: &[f32]) -> (f32, f64) {
    let start = Instant::now();
    let mut sum32: f32 = 0.0;
    let mut c32: f32 = 0.0;
    let mut sum64: f64 = 0.0;
    let mut c64: f64 = 0.0;
    for &f in numbers {
        let y32 = f - c32;
        let t32 = sum32 + y32;
        c32 = (t32 - sum32) - y32;
        sum32 = t32;
        let f64v = f as f64;
        let y64 = f64v - c64;
        let t64 = sum64 + y64;
        c64 = (t64 - sum64) - y64;
        sum64 = t64;
    }
    let elapsed = start.elapsed().as_secs_f64();
    println!("Sum (Kahan):     f32={sum32}  f64={sum64}");
    println!("Kahan time:      {elapsed:.3} seconds");
    (sum32, sum64)
}

fn main() {
    let mut count: u32 = 0;
    let mut nan_count: u32 = 0;
    let mut inf_count: u32 = 0;
    let mut numbers: Vec<f32> = Vec::new();

    let start = Instant::now();

    for bits in 0..=u32::MAX {
        let f = f32::from_bits(bits);

        if f.is_nan() { nan_count += 1; continue; }
        if f.is_infinite() { inf_count += 1; continue; }

        if (-1.0..=1.0).contains(&f) {
            count += 1;
            numbers.push(f);
        }
    }

    let elapsed = start.elapsed().as_secs_f64();

    println!("=== Brute Force: all u32 -> f32 ===");
    println!("Total patterns:  {}", 1u64 << 32);
    println!("In [-1, 1]:      {count}");
    println!("NaN patterns:    {nan_count}");
    println!("Inf patterns:    {inf_count}");
    println!("Collect time:    {elapsed:.3} seconds");

    // Analytical: exp 0..126 any mantissa both signs + exp 127 mantissa=0 both signs
    let analytical: u32 = 127 * (1u32 << 24) + 2;
    println!("\nAnalytical count: {analytical}");
    println!("Match: {}", count == analytical);

    println!();
    sum_naive(&numbers);
    println!();
    sum_sorted(&numbers);
    println!();
    sum_gauss(&numbers);
    println!();
    sum_random_pick(&numbers);
    println!();
    sum_kahan(&numbers);
}

```