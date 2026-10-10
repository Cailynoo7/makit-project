h=param("leg_height",31)
radius=param("leg_radius",5.2)
top_radius=param("leg_top_radius",4.2)
sx=param("leg_top_spacing_x",54)
sy=param("leg_top_spacing_y",39)
splay=param("leg_splay",5)
end_round=param("leg_end_rounding",3)
pw=param("leg_plate_width",64)
pd=param("leg_plate_depth",49)
pt=param("leg_plate_thickness",2.2)
pr=param("leg_plate_rounding",3)
embed=param("leg_plate_leg_overlap",1)
with BuildPart() as plate:
    with BuildSketch(Plane.XY.offset(h-embed)):
        RectangleRounded(pw,pd,pr)
    extrude(amount=pt)
base=plate.part
for a,b in [(-1,-1),(1,-1),(-1,1),(1,1)]:
    with BuildPart() as leg:
        with BuildSketch(Plane.XY):
            with Locations((a*(sx/2+splay),b*(sy/2+splay))):
                Circle(radius)
        with BuildSketch(Plane.XY.offset(h)):
            with Locations((a*sx/2,b*sy/2)):
                Circle(top_radius)
        loft()
        fillet(leg.edges(),end_round)
    base=base+leg.part
assert radius>top_radius
assert len(base.solids())==1
print("Leg lower/top diameters:",radius*2,top_radius*2,"mm; joining plate:",pw,pd,pt,"mm")
base.color=srgb("#251510")
publish("leg_base",base,"四腿与嵌入薄板",material="pla")
fit("leg_base","seat",kind="fused",reason="四条腿先一体连接薄板，薄板嵌入座面底部，顶部0.2mm接入座面")
