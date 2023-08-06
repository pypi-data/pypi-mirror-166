//! polynomial trajectory

/// cubic polynomial trajectory
#[repr(C)]
pub struct PolyTrack3 {
    /// time unit(s)
    pub t: [f64; 2],
    /// position
    pub q: [f64; 2],
    /// velocity
    pub v: [f64; 2],
    /// quantity
    k: [f64; 4],
}

extern "C" {
    fn a_polytrack3_init(ctx: *mut PolyTrack3, source: *const [f64; 3], target: *const [f64; 3]);
    fn a_polytrack3_pos(ctx: *mut PolyTrack3, ts: f64) -> f64;
    fn a_polytrack3_vec(ctx: *mut PolyTrack3, ts: f64) -> f64;
    fn a_polytrack3_acc(ctx: *mut PolyTrack3, ts: f64) -> f64;
    fn a_polytrack3_all(ctx: *mut PolyTrack3, ts: f64, out: *mut [f64; 3]);
}

/**
# Examples

```no_run
let ts = 0.5;
let source = [0.0, 0.0, 0.0];
let target = [1.0, 1.0, 1.0];
let mut a = liba::PolyTrack3::new(source, target);
println!("{},{},{}", a.pos(ts), a.vec(ts), a.acc(ts));
println!("{:?}", a.all(ts));
```
*/
impl PolyTrack3 {
    /// initialize function for cubic polynomial trajectory
    pub fn new(source: [f64; 3], target: [f64; 3]) -> Self {
        let mut ctx: Self = Self {
            t: [0.0; 2],
            q: [0.0; 2],
            v: [0.0; 2],
            k: [0.0; 4],
        };
        unsafe { a_polytrack3_init(&mut ctx, &source, &target) };
        ctx
    }

    /// process function for cubic polynomial trajectory position
    pub fn pos(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack3_pos(self, ts) }
    }

    /// process function for cubic polynomial trajectory velocity
    pub fn vec(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack3_vec(self, ts) }
    }

    /// process function for cubic polynomial trajectory acceleration
    pub fn acc(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack3_acc(self, ts) }
    }

    /// process function for cubic polynomial trajectory
    pub fn all(&mut self, ts: f64) -> [f64; 3] {
        let mut out: [f64; 3] = [0.0; 3];
        unsafe { a_polytrack3_all(self, ts, &mut out) };
        out
    }
}

/// quintic polynomial trajectory
#[repr(C)]
pub struct PolyTrack5 {
    /// time unit(s)
    pub t: [f64; 2],
    /// position
    pub q: [f64; 2],
    /// velocity
    pub v: [f64; 2],
    /// acceleration
    pub a: [f64; 2],
    /// quantity
    k: [f64; 6],
}

extern "C" {
    fn a_polytrack5_init(ctx: *mut PolyTrack5, source: *const [f64; 4], target: *const [f64; 4]);
    fn a_polytrack5_pos(ctx: *mut PolyTrack5, ts: f64) -> f64;
    fn a_polytrack5_vec(ctx: *mut PolyTrack5, ts: f64) -> f64;
    fn a_polytrack5_acc(ctx: *mut PolyTrack5, ts: f64) -> f64;
    fn a_polytrack5_all(ctx: *mut PolyTrack5, ts: f64, out: *mut [f64; 3]);
}

/**
# Examples

```no_run
let ts = 0.5;
let source = [0.0, 0.0, 0.0, 0.0];
let target = [1.0, 1.0, 1.0, 1.0];
let mut a = liba::PolyTrack5::new(source, target);
println!("{},{},{}", a.pos(ts), a.vec(ts), a.acc(ts));
println!("{:?}", a.all(ts));
```
*/
impl PolyTrack5 {
    /// initialize function for quintic polynomial trajectory
    pub fn new(source: [f64; 4], target: [f64; 4]) -> Self {
        let mut ctx: Self = Self {
            t: [0.0; 2],
            q: [0.0; 2],
            v: [0.0; 2],
            a: [0.0; 2],
            k: [0.0; 6],
        };
        unsafe { a_polytrack5_init(&mut ctx, &source, &target) };
        ctx
    }

    /// process function for quintic polynomial trajectory position
    pub fn pos(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack5_pos(self, ts) }
    }

    /// process function for quintic polynomial trajectory velocity
    pub fn vec(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack5_vec(self, ts) }
    }

    /// process function for quintic polynomial trajectory acceleration
    pub fn acc(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack5_acc(self, ts) }
    }

    /// process function for quintic polynomial trajectory
    pub fn all(&mut self, ts: f64) -> [f64; 3] {
        let mut out: [f64; 3] = [0.0; 3];
        unsafe { a_polytrack5_all(self, ts, &mut out) };
        out
    }
}

/// hepta polynomial trajectory
#[repr(C)]
pub struct PolyTrack7 {
    /// time unit(s)
    pub t: [f64; 2],
    /// position
    pub q: [f64; 2],
    /// velocity
    pub v: [f64; 2],
    /// acceleration
    pub a: [f64; 2],
    /// jerk
    pub j: [f64; 2],
    /// quantity
    k: [f64; 8],
}

extern "C" {
    fn a_polytrack7_init(ctx: *mut PolyTrack7, source: *const [f64; 5], target: *const [f64; 5]);
    fn a_polytrack7_pos(ctx: *mut PolyTrack7, ts: f64) -> f64;
    fn a_polytrack7_vec(ctx: *mut PolyTrack7, ts: f64) -> f64;
    fn a_polytrack7_acc(ctx: *mut PolyTrack7, ts: f64) -> f64;
    fn a_polytrack7_jer(ctx: *mut PolyTrack7, ts: f64) -> f64;
    fn a_polytrack7_all(ctx: *mut PolyTrack7, ts: f64, out: *mut [f64; 4]);
}

/**
# Examples

```no_run
let ts = 0.5;
let source = [0.0, 0.0, 0.0, 0.0, 0.0];
let target = [1.0, 1.0, 1.0, 1.0, 1.0];
let mut a = liba::PolyTrack7::new(source, target);
println!("{},{},{},{}", a.pos(ts), a.vec(ts), a.acc(ts), a.jer(ts));
println!("{:?}", a.all(ts));
```
*/
impl PolyTrack7 {
    /// initialize function for hepta polynomial trajectory
    pub fn new(source: [f64; 5], target: [f64; 5]) -> Self {
        let mut ctx: Self = Self {
            t: [0.0; 2],
            q: [0.0; 2],
            v: [0.0; 2],
            a: [0.0; 2],
            j: [0.0; 2],
            k: [0.0; 8],
        };
        unsafe { a_polytrack7_init(&mut ctx, &source, &target) };
        ctx
    }

    /// process function for hepta polynomial trajectory position
    pub fn pos(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack7_pos(self, ts) }
    }

    /// process function for hepta polynomial trajectory velocity
    pub fn vec(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack7_vec(self, ts) }
    }

    /// process function for hepta polynomial trajectory acceleration
    pub fn acc(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack7_acc(self, ts) }
    }

    /// process function for hepta polynomial trajectory jerk
    pub fn jer(&mut self, ts: f64) -> f64 {
        unsafe { a_polytrack7_jer(self, ts) }
    }

    /// process function for hepta polynomial trajectory
    pub fn all(&mut self, ts: f64) -> [f64; 4] {
        let mut out: [f64; 4] = [0.0; 4];
        unsafe { a_polytrack7_all(self, ts, &mut out) };
        out
    }
}
