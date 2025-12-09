// ==========================================
// Catenary Generation Functions
// ==========================================

// Helper functions: Hyperbolic Trigonometry
function sinh(x)  = (exp(x) - exp(-x)) / 2;
function cosh(x)  = (exp(x) + exp(-x)) / 2;
function asinh(x) = ln(x + sqrt(x * x + 1));

// Helper function: Recursive Binary Search to find the parameter 'z'
// Solves sinh(z)/z = target
function solve_catenary_z(target, low=0.0001, high=50, steps=30) =
    steps <= 0 ? (low + high) / 2 :
    let(
        mid = (low + high) / 2,
        val = sinh(mid) / mid
    )
    (val < target) ? 
        solve_catenary_z(target, mid, high, steps - 1) : 
        solve_catenary_z(target, low, mid, steps - 1);

/*
    Generates a list of 3D points forming a catenary curve.
    
    Args:
        p1 (vector): Start point [x, y, z]
        p2 (vector): End point [x, y, z]
        slackness (float): Ratio of curve length to straight-line distance (> 1.0)
        spacing (float): Approximate distance between points
        
    Returns:
        List of [x, y, z] vectors
*/
function catenary_points(p1, p2, slackness=1.2, spacing=1) = 
    let(
        // 1. Calculate dimensions in the vertical plane
        vec = p2 - p1,
        dist_straight = norm(vec),
        
        // Horizontal distance on the XY plane
        h_dist = norm([vec.x, vec.y]), 
        // Vertical distance
        v_dist = vec.z,
        
        // Actual length of the curve
        // Ensure slackness is at least slightly > 1 to avoid division by zero errors
        safe_slack = max(slackness, 1.0001),
        curve_len = dist_straight * safe_slack
    )
    // Edge case: Vertical alignment (infinite tension for finite 'a')
    // We return a straight line if h_dist is near zero or slackness is 1
    (h_dist < 0.001 || safe_slack <= 1.0001) ? [p1, p2] :
    let(
        // 2. Solve for Catenary Parameters
        // We need to find 'a' (scaling factor) and (x0, y0) (vertex offset)
        // Based on equation: sqrt(Length^2 - V_dist^2) = 2a * sinh(H_dist / 2a)
        
        // K is the projection of the arc length onto the horizontal-equivalent tension domain
        K = sqrt(pow(curve_len, 2) - pow(v_dist, 2)),
        
        // We solve for z = h_dist / (2a)
        // Target ratio for the solver: sinh(z)/z = K / h_dist
        target_ratio = K / h_dist,
        z = solve_catenary_z(target_ratio),
        
        // Calculate the Catenary Constant 'a'
        a = h_dist / (2 * z),
        
        // Calculate the vertex offsets (x0, y0) in the local 2D plane
        // x0 is the horizontal distance from p1 to the curve's lowest point
        x0 = h_dist / 2 - a * asinh(v_dist / K),
        y0 = -a * cosh(x0 / a), // Offset so that local_y(0) starts at 0 relative shift
        
        // 3. Generate Points
        num_segments = max(1, round(curve_len / spacing)),
        step_u = h_dist / num_segments,
        
        // Unit vector for horizontal direction on XY plane
        h_dir = [vec.x, vec.y, 0] / h_dist
    )
    [
        for (i = [0 : num_segments])
        let(
            // u is the horizontal distance along the line connecting p1_xy and p2_xy
            u = i * step_u,
            
            // Calculate height in local 2D coordinates
            // Standard Catenary: y = a * cosh((x - x0) / a) + y0
            local_z = a * cosh((u - x0) / a) + y0
        )
        // Map back to 3D: P1 + Horizontal_Vector * u + Vertical_Offset
        p1 + h_dir * u + [0, 0, local_z]
    ];

// ==========================================
// Example Usage
// ==========================================

// Define parameters
pt_start = [0, 0, 20];
pt_end   = [80, 50, 40];
slack    = 1.25;
step     = 2;

module catenary(pt_start, pt_end, slack, step, thickness=1.5) {
    // Generate the points
    points = catenary_points(pt_start, pt_end, slack, step);

    // Visualization Module
    module draw_chain(pts, thickness=1) {
        // Iterate through points and connect them
        for (i = [0 : len(pts) - 2]) {
            hull()
            {
                translate(pts[i]) sphere(d=thickness);
                translate(pts[i+1]) sphere(d=thickness);
            }
        }
    }
    
    draw_chain(points, thickness);
}

// 1. Draw the reference poles
color([0.7, 0.7, 0.7]) {
    translate([pt_start.x, pt_start.y, 0]) cylinder(h=pt_start.z, d=2);
    translate([pt_end.x, pt_end.y, 0]) cylinder(h=pt_end.z, d=2);
}

// 2. Draw the endpoints
color("red") {
    translate(pt_start) sphere(d=3);
    translate(pt_end) sphere(d=3);
}

// 3. Draw the calculated catenary curve
color("gold") 
catenary(pt_start, pt_end, slack, step);
