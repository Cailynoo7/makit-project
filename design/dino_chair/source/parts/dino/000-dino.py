w=param("dino_width",48)
h=param("dino_height",58)
t=param("dino_thickness",13)
edge=param("dino_edge_radius",2)
gap=param("dino_foot_gap",12)
fh=param("dino_foot_gap_height",9)
tw=param("tail_reach",17)
tr=param("tail_root_radius",5.6)
rise=param("tail_tip_height",10.5)
fr=param("foot_gap_rounding",1.2)
dip=param("tail_mid_dip",1.3)
tip_r=param("tail_tip_round_radius",1.1)
fullness=param("dino_head_fullness",1.2)
crown_rise=param("dino_crown_rise",22)
backing_w=param("muzzle_backing_width",51)
backing_h=param("muzzle_backing_height",32.714)
backing_x=param("muzzle_backing_center_x",-8.5)
backing_z=param("muzzle_backing_center_z",22.857)
shoulder_inset=param("muzzle_side_shoulder_inset",1.5)
cheek_land=param("muzzle_side_backing_extra",1)
cheek_drop=param("muzzle_side_lower_cheek_drop",1.5)
head_cz=h-crown_rise
left_cheek_fullness=param("dino_own_left_cheek_fullness",3.8)
insert=param("dino_foot_insert_depth",4)
seat_top_local=param("dino_seat_top_local_z",2)
bottom_z=seat_top_local-insert
with BuildPart() as bp:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            cx=-w/48
            r=w/2+fullness
            left_x=backing_x-backing_w/2-cheek_land
            # Hard leg-root corner; tangent cheek-to-crown junction.
            Bezier((-w*.36,fh-cheek_drop),(left_x,fh-cheek_drop),(left_x,backing_z),weights=[1,2**-.5,1])
            Bezier((left_x,backing_z),(left_x,backing_z+backing_h*.32),(cx-r+shoulder_inset,head_cz-7),(cx-r+shoulder_inset,head_cz))
            # Rational quarter curves form one tangent- and curvature-continuous oval crown.
            Bezier((cx-r+shoulder_inset,head_cz),(cx-r+shoulder_inset,h),(cx,h),weights=[1,2**-.5,1])
            # A continuous outward-convex cheek restores a rounded, full silhouette.
            Bezier((cx,h),(cx+r+left_cheek_fullness,h),(cx+r+left_cheek_fullness,fh+(head_cz-fh)*.75),(w*.43,fh))
            Polyline((w*.43,fh),(w*.43,bottom_z),(-w*.36,bottom_z),(-w*.36,fh-cheek_drop))
        make_face()
    extrude(amount=t)
crotch_z=fh-cheek_drop
with BuildPart() as opening:
    with BuildSketch(Plane.XZ):
        with Locations(((w*.43-w*.36)/2,(crotch_z+bottom_z-1)/2)):
            RectangleRounded(gap,crotch_z-bottom_z+1,fr)
    extrude(amount=t+2,both=True)
body=bp.part-opening.part
# Roll front/back perimeter down both outer and inner leg sides; leave foot soles sharp.
side_edges=[e for e in body.edges().filter_by(Axis.Y,reverse=True) if e.bounding_box().max.Z>bottom_z+1e-5]
body=fillet(side_edges,edge)
print("Body and leg side radius:",edge,"mm; sole plane:",bottom_z,"mm")
foot_left=-w*.36
foot_right=w*.43
foot_mid=(foot_left+foot_right)/2
left_foot_width=foot_mid-gap/2-foot_left
right_foot_width=foot_right-(foot_mid+gap/2)
assert abs(left_foot_width-right_foot_width)<1e-8
print("Foot gap:",gap,"mm; both foot widths:",left_foot_width,"mm")
# Tail keeps its length, dips gently and closes with an integrated round cap.
from math import sqrt
root_x=w*.37
tip_x=w/2+tw
cap_x=tip_x-tip_r
root_z=tr
low_z=root_z-dip
with BuildPart() as tail:
    stations=[
        (root_x,tr,root_z),
        (root_x+(cap_x-root_x)*.15,tr*.90,root_z-dip*.55),
        (root_x+(cap_x-root_x)*.35,tr*.74,low_z),
        (root_x+(cap_x-root_x)*.55,tr*.57,low_z+(rise-low_z)*.12),
        (root_x+(cap_x-root_x)*.75,tr*.44,low_z+(rise-low_z)*.42),
        (root_x+(cap_x-root_x)*.90,tr*.34,low_z+(rise-low_z)*.83),
        (root_x+(cap_x-root_x)*.96,tip_r*1.04,rise),
        (cap_x,tip_r,rise)]
    for xx,rr,zz in stations:
        with BuildSketch(Plane.YZ.offset(xx)):
            with Locations((-t/2,zz)):
                Circle(rr)
    loft()
rounded_tail=tail.part+Pos(cap_x,-t/2,rise)*Sphere(tip_r)
assert len(rounded_tail.solids())==1
# Only hidden material below the seat outside the right foot is relieved.
relief=Pos((foot_right+tip_x+tip_r)/2,-t/2,seat_top_local-(tr+t)/2)*Box(tip_x+tip_r-foot_right,t+2*tr,tr+t)
rounded_tail=rounded_tail-relief
body=body+rounded_tail
assert len(body.solids())==1
radius=param("spine_radius",3.4)
length=param("spine_length",7.5)
tip=param("spine_tip_radius",0.55)
rounding=param("spine_rounding",0.45)
top_z=param("top_spine_height",56.5)
second_z=param("second_spine_height",52.8)
seventh=param("seventh_spine_scale",0.7)
tail_z1=param("tail_spine_1_height",7.2)
tail_z2=param("tail_spine_2_height",6.8)
tail_x1=param("tail_spine_1_x",26)
tail_spacing=param("tail_spine_spacing",6)
positions=[(4,top_z,14),(15,second_z,32),(21,46,65),(23,38,82),(23.5,30,90),(22.7,22,95),(21,14,102),(tail_x1,tail_z1,35),(tail_x1+tail_spacing,tail_z2,20)]
side_inset=param("spine_side_inset",1.2)
pieces=[]
for i,(x,z,angle) in enumerate(positions):
    if 1<=i<=6:
        x-=side_inset
    size=seventh if i==6 else (1 if i<6 else .65)
    rr=radius*size
    ll=length*size
    with BuildPart() as bp:
        with BuildSketch(Plane.XZ):
            with BuildLine():
                Polyline((0,0),(rr,0))
                Spline((rr,0),(rr*1.02,ll*.22),(rr*.77,ll*.60),(tip*size+rounding*size,ll*.91),(0,ll))
                Line((0,ll),(0,0))
            make_face()
        revolve(axis=Axis.Z)
    pieces.append(Pos(x,-t/2,z)*Rot(0,angle,0)*bp.part)

assert len(pieces)==9
for spine_piece in pieces:
    body=body+spine_piece
assert len(body.solids())==1, "All nine spines must fuse into the dinosaur body"
print("Nine spines boolean-unioned into one dinosaur solid")
body.color=srgb("#24a84e")
publish("dino",body,"恐龙主体与九枚背刺",material="pla")
