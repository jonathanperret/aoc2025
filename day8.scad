include <day8.inc>

echo(len(boxes), len(links));

s = 0.001;
d = 2;

*for(box = boxes) {
    pos = s * box;
    translate([pos[0], pos[1], pos[2]])
    cube(d, center=true);
}

echo($t);
for(i = [0:len(links)-1]) {
    link = links[i];
    hull() {
        for(i = link) {
            box = boxes[i];
            pos = s * box;
            translate([pos[0], pos[1], pos[2]])
            //cube(d, center=true);
            sphere(d=d, $fn=1);
        }
    }
}
