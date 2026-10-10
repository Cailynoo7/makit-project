w=param("eye_width",3.6)
h=param("eye_height",4.4)
depth=param("eye_depth",1.1)
spacing=param("eye_spacing",8)
left=param("eye_left_shift",1.2)
face_y=param("eye_face_contact_local_y",0.1)
# Elliptical sections preserve the original ellipsoid dimensions and avoid
# the affine-transformed sphere's STEP trimming inversion.
fractions=[-0.499999,-0.499,-0.495,-0.485,-0.47,-0.45,-0.425,-0.4,-0.35,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.425,0.45,0.47,0.485,0.495,0.499,0.499999]
cutter=Pos(0,face_y,0)*Box(4*w,4*depth,4*h,align=(Align.CENTER,Align.MIN,Align.CENTER))
for i,x in enumerate([-spacing/2-left,spacing/2-left]):
    with BuildPart() as ellipsoid:
        for f in fractions:
            scale=(1-(2*f)**2)**0.5
            with BuildSketch(Plane.XZ.offset(-depth*f)):
                with Locations((x,0)):
                    Ellipse(w*scale/2,h*scale/2)
        loft()
    original=ellipsoid.part
    eye=original-cutter
    assert len(eye.solids())==1
    assert original.volume-eye.volume>0
    assert eye.center().Y<face_y
    eye.color=srgb("#35201a")
    publish("eye_"+str(i+1),eye,"裁切深棕眼睛 "+str(i+1),material="pla")
