from math import sqrt, atan, cos, sin, pi
r=param("horn_base_radius",4.8)
h=param("horn_height",15)
tip_r=param("horn_tip_round_radius",1.1)
lean=param("horn_forward_lean_deg",8)
side_lean=param("horn_side_lean_deg",5)
# A tapered cone meets its rounded cap tangentially, without a pinched neck.
zc=h-tip_r
slope=(r*zc-tip_r*sqrt(zc*zc+r*r-tip_r*tip_r))/(zc*zc-tip_r*tip_r)
angle=atan(slope)
tx=tip_r*cos(angle)
tz=zc+tip_r*sin(angle)
mid_angle=(angle+pi/2)/2
with BuildPart() as hp:
    with BuildSketch(Plane.XZ):
        with BuildLine():
            Polyline((0,0),(r,0),(tx,tz))
            ThreePointArc((tx,tz),(tip_r*cos(mid_angle),zc+tip_r*sin(mid_angle)),(0,h))
            Line((0,h),(0,0))
        make_face()
    revolve(axis=Axis.Z)
horn=Rot(lean,-side_lean,0)*hp.part
# Head cutter reconstructed from the exact v39 source and parameter snapshot.
# Update this reference if the head silhouette or edge radius changes.
def head_contact_tool():
    w=48
    h=58
    t=13
    edge=1
    gap=16
    fh=9
    tw=17
    tr=5.6
    rise=8.5
    fr=1.2
    dip=1.3
    tip_r=1.6
    fullness=1.2
    crown_rise=18
    backing_w=53.35
    backing_h=30.011885
    backing_x=-9.5
    backing_z=22.16415
    shoulder_inset=1.5
    cheek_land=1
    cheek_drop=1.5
    head_cz=h-crown_rise
    left_cheek_fullness=3.8
    insert=4
    seat_top_local=2
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
    
    return body
head_x=param("horn_head_relative_x",8)
head_y=param("horn_head_relative_y",7)
head_z=param("horn_head_relative_z",-56)
head_tool=Pos(head_x,head_y,head_z)*head_contact_tool()
uncut_volume=horn.volume
horn=horn-head_tool
assert len(horn.solids())==1 and uncut_volume-horn.volume>50
print("Horn buried volume removed:",uncut_volume-horn.volume,"mm3")
assert len(horn.solids())==1
horn.color=srgb("#fff0d3")
publish("horn",horn,"参考图圆头锥形独角",material="pla")

