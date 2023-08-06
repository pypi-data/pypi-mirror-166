// Code from https://rust-lang-nursery.github.io/rust-cookbook/science/mathematics/statistics.html#statistics
use std::cmp::Ordering;
use anyhow::{Result, anyhow};

fn partition(data: &[f32]) -> Option<(Vec<f32>, f32, Vec<f32>)> {
    match data.len() {
        0 => None,
        _ => {
            let (pivot_slice, tail) = data.split_at(1);
            let pivot = pivot_slice[0];
            let (left, right) = tail.iter()
                .fold((vec![], vec![]), |mut splits, next| {
                    {
                        let (ref mut left, ref mut right) = &mut splits;
                        if next < &pivot {
                            left.push(*next);
                        } else {
                            right.push(*next);
                        }
                    }
                    splits
                });

            Some((left, pivot, right))
        }
    }
}

fn select(data: &[f32], k: usize) -> Option<f32> {
    let part = partition(data);

    match part {
        None => None,
        Some((left, pivot, right)) => {
            let pivot_idx = left.len();

            match pivot_idx.cmp(&k) {
                Ordering::Equal => Some(pivot),
                Ordering::Greater => select(&left, k),
                Ordering::Less => select(&right, k - (pivot_idx + 1)),
            }
        },
    }
}

pub fn median(data: &[f32], size: usize) -> Result<f32> {
    // let size = data.len();

    match size {
        even if even % 2 == 0 => {
            let fst_med = select(data, (even / 2) - 1);
            let snd_med = select(data, even / 2);

            match (fst_med, snd_med) {
                (Some(fst), Some(snd)) => Ok((fst + snd) as f32 / 2.0),
                _ => Err(anyhow!("Unvalid input"))
            }
        },
        odd => Ok(select(data, odd / 2).map(|x| x as f32).unwrap())
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_median() {
        let data: [f32; 10] = [3.0, 1.0, 6.0, 1.0, 5.0, 8.0, 1.0, 8.0, 10.0, 11.0];

        let part = partition(&data);
        println!("Partition is {:?}", part);

        let sel = select(&data, 5);
        println!("Selection at ordered index {} is {:?}", 5, sel);

        let med = median(&data, 10);
        println!("Median is {:?}", med);
    }
}