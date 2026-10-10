w=param("muzzle_width",47)
h=param("muzzle_height",27)
d=param("muzzle_depth",17)
nr=param("nostril_radius",0.9)
spacing=param("nostril_spacing",6)
vertical_bulge=param("muzzle_vertical_bulge",1.4)
front_bulge=param("muzzle_front_bulge",2.5)
full_h=h+2*vertical_bulge
full_d=d+front_bulge
centre_y=-full_d/2
end_power=param("muzzle_end_profile_power",2.8)
sections=[]
for fraction in [-.5,-.495,-.48,-.45,-.4,-.35,-.25,-.125,0,.125,.25,.35,.4,.45,.48,.495,.5]:
    scale=max(.01,(1-abs(2*fraction)**end_power)**0.5)
    with BuildSketch(Plane.YZ.offset(w*fraction)) as section:
        with Locations((centre_y,0)):
            Ellipse(full_d/2*scale,full_h/2*scale)
    sections.append(section.sketch)
shape=loft(sections)
for x in [-w*.26,-w*.26+spacing]:
    shape=shape-(Pos(x,-full_d+0.5,h*.20)*Rot(90,0,0)*Cylinder(nr,7))
face_y=param("muzzle_face_contact_local_y",-7.5) # face Y14 in muzzle frame at Y21.5
buried=Pos(0,face_y+full_d,0)*Box(2*w,2*full_d,2*full_h)
uncut_volume=shape.volume
shape=shape-buried
assert len(shape.solids())==1 and shape.volume>1000
assert uncut_volume-shape.volume>5000
print("Removed buried volume:",uncut_volume-shape.volume,"mm3; mating plane local Y:",face_y)
shape.color=srgb("#fff0d3")
publish("muzzle",shape,"中央微鼓鼻嘴",material="pla")
