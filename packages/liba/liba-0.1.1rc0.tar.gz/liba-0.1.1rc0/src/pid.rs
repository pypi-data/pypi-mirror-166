//! proportional integral derivative controller

/// turn off PID controller
pub const OFF: u32 = 0;
/// positional PID controller
pub const POS: u32 = 1;
/// incremental PID controller
pub const INC: u32 = 2;

/// proportional integral derivative controller
#[repr(C)]
pub struct PID {
    /// sampling time unit(s)
    pub ts: f64,
    /// proportional constant
    pub kp: f64,
    /// integral constant
    pub ki: f64,
    /// derivative constant
    pub kd: f64,
    /// controller output
    pub out: f64,
    /// minimum output
    pub outmin: f64,
    /// maximum output
    pub outmax: f64,
    /// maximum integral output
    pub summax: f64,
    /// (integral) output item sum
    pub sum: f64,
    /// cache feedback
    pub r#ref: f64,
    /// error change
    pub ec: f64,
    /// error input
    pub e: f64,
    mode: u32,
}

extern "C" {
    fn a_pid_off(ctx: *mut PID) -> *mut PID;
    fn a_pid_inc(ctx: *mut PID) -> *mut PID;
    fn a_pid_pos(ctx: *mut PID, max: f64) -> *mut PID;
    fn a_pid_mode(ctx: *mut PID, mode: u32) -> *mut PID;
    fn a_pid_time(ctx: *mut PID, ts: f64) -> *mut PID;
    fn a_pid_kpid(ctx: *mut PID, kp: f64, ki: f64, kd: f64) -> *mut PID;
    fn a_pid_proc(ctx: *mut PID, set: f64, r#ref: f64) -> f64;
    fn a_pid_done(ctx: *mut PID) -> *mut PID;
}

/**
## Examples

```no_run
let mut pid = liba::PID::new(1.0, -10.0, 10.0);
pid.mode(liba::pid::OFF);
pid.mode(liba::pid::POS);
pid.mode(liba::pid::INC);
pid.kpid(10.0, 0.1, 1.0);
pid.time(0.1);
pid.pos(10.0);
pid.off();
pid.inc();
pid.proc(1.0, 0.0);
pid.done();
```
*/
impl PID {
    /// initialize function for PID controller, default is turn off
    pub fn new(ts: f64, outmin: f64, outmax: f64) -> Self {
        Self {
            ts,
            outmin,
            outmax,
            kp: 0.0,
            ki: 0.0,
            kd: 0.0,
            out: 0.0,
            summax: 0.0,
            sum: 0.0,
            r#ref: 0.0,
            ec: 0.0,
            e: 0.0,
            mode: OFF,
        }
    }

    /// initialize function for positional PID controller
    pub fn new_pos(
        ts: f64,
        kp: f64,
        ki: f64,
        kd: f64,
        outmin: f64,
        outmax: f64,
        summax: f64,
    ) -> Self {
        Self {
            ts,
            kp,
            ki,
            kd,
            outmin,
            outmax,
            summax,
            mode: POS,
            out: 0.0,
            sum: 0.0,
            r#ref: 0.0,
            ec: 0.0,
            e: 0.0,
        }
    }

    /// initialize function for incremental PID controller
    pub fn new_inc(ts: f64, kp: f64, ki: f64, kd: f64, outmin: f64, outmax: f64) -> Self {
        Self {
            ts,
            kp,
            ki,
            kd,
            outmin,
            outmax,
            mode: INC,
            out: 0.0,
            summax: 0.0,
            sum: 0.0,
            r#ref: 0.0,
            ec: 0.0,
            e: 0.0,
        }
    }

    /// set turn off mode
    pub fn off(&mut self) -> &mut PID {
        unsafe { a_pid_off(self).as_mut().unwrap_unchecked() }
    }

    /// set incremental mode
    pub fn inc(&mut self) -> &mut PID {
        unsafe { a_pid_inc(self).as_mut().unwrap_unchecked() }
    }

    /// set positional mode
    pub fn pos(&mut self, max: f64) -> &mut PID {
        unsafe { a_pid_pos(self, max).as_mut().unwrap_unchecked() }
    }

    /// set mode for PID controller
    pub fn mode(&mut self, mode: u32) -> &mut PID {
        unsafe { a_pid_mode(self, mode).as_mut().unwrap_unchecked() }
    }

    /// set sampling period for PID controller
    pub fn time(&mut self, ts: f64) -> &mut PID {
        unsafe { a_pid_time(self, ts).as_mut().unwrap_unchecked() }
    }

    /// set proportional integral derivative constant for PID controller
    pub fn kpid(&mut self, kp: f64, ki: f64, kd: f64) -> &mut PID {
        unsafe { a_pid_kpid(self, kp, ki, kd).as_mut().unwrap_unchecked() }
    }

    /// process function for PID controller
    pub fn proc(&mut self, set: f64, r#ref: f64) -> f64 {
        unsafe { a_pid_proc(self, set, r#ref) }
    }

    /// terminate function for PID controller
    pub fn done(&mut self) -> &mut PID {
        unsafe { a_pid_done(self).as_mut().unwrap_unchecked() }
    }
}
