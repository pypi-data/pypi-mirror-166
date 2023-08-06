use std::env;

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();
    println!("cargo:rustc-flags=-L {}/lib64/ -L {}/lib/", &out_dir, &out_dir);
}