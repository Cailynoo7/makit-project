w=param("seat_width",80)
d=param("seat_depth",65)
t=param("seat_thickness",11)
r=param("seat_rounding",4)
side_r=param("seat_side_rounding",12)
gr=param("groove_radius",6.5)
pitch=param("groove_pitch",13)
depth=param("groove_depth",4.5)
rear_start=param("rear_platform_start",12.5)
middle_shift=param("groove_middle_rear_shift",2)
front=param("seat_front_extension",3)
blank=Pos(0,-front/2,0)*Box(w,d+front,t)
seat=fillet(blank.edges().filter_by(Axis.Z),side_r)
rim_edges=[e for e in seat.edges() if abs(abs(e.center().Z)-t/2)<1e-6]
seat=fillet(rim_edges,r)
half_opening=(gr**2-(gr-depth)**2)**0.5
reference_half_opening=6.0 # v31 groove-position datum; diameter changes do not move centres
last_center=rear_start-reference_half_opening
groove_centres=[last_center-2*pitch,last_center-pitch+middle_shift]
for y in groove_centres:
    seat=seat-(Pos(0,y,t/2+gr-depth)*Rot(0,90,0)*Cylinder(gr,w+4))
actual_rear_start=groove_centres[-1]+half_opening
assert groove_centres[-1]-groove_centres[0]>2*half_opening
print("Rear flat platform:",actual_rear_start,"to",d/2-r,"mm; groove centres:",groove_centres)
pw=param("seat_leg_plate_pocket_width",64)
pd=param("seat_leg_plate_pocket_depth",49)
pt=param("seat_leg_plate_pocket_height",2)
pr=param("seat_leg_plate_pocket_rounding",3)
with BuildPart() as pocket:
    with BuildSketch(Plane.XY.offset(-t/2-.1)):
        RectangleRounded(pw,pd,pr)
    extrude(amount=pt+.1)
seat=seat-pocket.part
fw=param("seat_dino_foot_width",10.96)
ft=param("seat_dino_foot_thickness",13)
fg=param("seat_dino_foot_gap",16)
fx=param("seat_dino_frame_x",-2.4125)
fy=param("seat_dino_foot_center_y",20.5)
mid=param("seat_dino_foot_mid_local_x",1.68)
sd=param("seat_dino_slot_depth",4.2)
clear=param("seat_dino_slot_side_clearance",0.2)
foot_side_r=param("seat_dino_foot_side_radius",1)
slot_r=foot_side_r+clear
for xx in [fx+mid-(fg+fw)/2,fx+mid+(fg+fw)/2]:
    with BuildPart() as slot:
        with BuildSketch(Plane.XY.offset(t/2-sd)):
            with Locations((xx,fy)):
                RectangleRounded(fw+2*clear,ft+2*clear,slot_r)
        extrude(amount=sd+.1)
    seat=seat-slot.part
print("Leg side radius:",foot_side_r,"mm; matching slot radius:",slot_r,"mm")
assert len(seat.solids())==1
print("Dino slots:",fw+2*clear,ft+2*clear,sd,"mm; side clearance:",clear)
print("Groove diameter:",2*gr,"mm; bottom pocket:",pw,pd,pt)
print("Seat bounds Y:",-d/2-front,d/2,"mm; groove centres:",groove_centres)
seat.color=srgb("#fff0d3")
publish("seat",seat,"双槽座面与后端平面",material="pla")