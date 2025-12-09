include <day8.inc>
use <day8_renders/catenary.scad>

echo(len(boxes), len(links));

s = 0.001;
d = 1;
slack = 1.5;
step = 1;


*for(box = boxes) {
    pos = s * box;
    translate([pos[0], pos[1], pos[2]])
    cube(d, center=true);
}

for(i = [0:len(links)-1]) { //len(links)-1]) {
    link = links[i];
    $fn=8;
    catenary(s*boxes[link[0]], s*boxes[link[1]], slack, step=step, thickness=d);
    *hull() {
        for(i = link) {
            box = boxes[i];
            pos = s * box;
            translate([pos[0], pos[1], pos[2]])
            //cube(d, center=true);
            sphere(d=d, $fn=5);
        }
    }
}
