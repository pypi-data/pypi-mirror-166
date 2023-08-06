import spiceypy as sp
import numpy as np


d2r = 3.141592653589793/180
r2d = 180/3.141592653589793
   

def lonlat_to_cartesian(obs_loc):
    """
    obs_loc : (lon (deg), lat (deg), alt (m))
    """
    lon, lat, alt = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    alt = alt / 1000
    radii = [6378.1366, 6378.1366, 6356.7519]
    re = radii[0]
    rp = radii[2]
    f = (re-rp)/re
    obspos = sp.pgrrec(body='earth', lon=lon, lat=lat, alt=alt, re=re, f=f)
    return obspos


##def get_icrs(body, t, kernels):
##    for k in kernels:
##        sp.furnsh(k)
##    et = sp.str2et(str(t))
##    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr='NONE', obs=0)
##    pos = state[:3]
##    vel = state[3:]
##    sp.kclear()
##    return pos, vel, lt


##def get_topocentric(body, t, obs_loc, kernels):
##    r,az,alt = get_apparent(body, t, obs_loc, kernels, abcorr='NONE')
##    for k in kernels:
##        sp.furnsh(k)
##    topo = sp.azlrec(range=r, az=az*d2r, el=alt*d2r,
##                     azccw=False, elplsz=True)
##    sp.kclear()
##    return topo


def get_apparent(body, t, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))
    
    state, lt  = sp.azlcpo(
        method='ELLIPSOID',
        target=body,
        et=et,
        abcorr=abcorr,
        azccw=False,
        elplsz=True,
        obspos=lonlat_to_cartesian(obs_loc),
        obsctr='earth',
        obsref='ITRF93')

    r, az, alt = state[:3]

    sp.kclear()

    return r, az*r2d, alt*r2d


def get_apparent_bodies(bodies, t, obs_loc, kernels, abcorr='LT+S'):

    bodies = [str(i) for i in bodies]

    for k in kernels:
        sp.furnsh(k)

    et = sp.str2et(str(t))
    obspos = lonlat_to_cartesian(obs_loc)

    r_az_alt = np.zeros((len(bodies),3))

    for i in range(len(bodies)):
        state, lt  = sp.azlcpo(
            method='ELLIPSOID',
            target=bodies[i],
            et=et,
            abcorr=abcorr,
            azccw=False,
            elplsz=True,
            obspos=obspos,
            obsctr='earth',
            obsref='ITRF93')
        r, az, alt = state[:3]
        r_az_alt[i,:] = r, az*r2d, alt*r2d

    sp.kclear()

    return r_az_alt


def get_apparent_window(body, t1, t2, steps, obs_loc, kernels, abcorr='LT+S'):

    if isinstance(body, int):
        body = str(body)

    for k in kernels:
        sp.furnsh(k)

    et1 = sp.str2et(str(t1))
    et2 = sp.str2et(str(t2))
    t_win = np.linspace(et1, et2, steps)
    
    obspos = lonlat_to_cartesian(obs_loc)

    r_az_alt = np.zeros((len(t_win),3))

    for i in range(len(t_win)):
        state, lt  = sp.azlcpo(
            method='ELLIPSOID',
            target=body,
            et=t_win[i],
            abcorr=abcorr,
            azccw=False,
            elplsz=True,
            obspos=obspos,
            obsctr='earth',
            obsref='ITRF93')
        r, az, alt = state[:3]
        r_az_alt[i,:] = r, az*r2d, alt*r2d

    sp.kclear()

    return r_az_alt


def gcrs_to_altaz(t, obs_loc, pos_gcrs, kernels=None):
    # Calculate ecef2enu rotation matrix
    lon, lat, _ = obs_loc
    lon = lon * d2r
    lat = lat * d2r
    r1 = [-np.sin(lon), np.cos(lon), 0]
    r2 = [-np.cos(lon)*np.sin(lat), -np.sin(lon)*np.sin(lat), np.cos(lat)]
    r3 = [np.cos(lon)*np.cos(lat), np.sin(lon)*np.cos(lat), np.sin(lat)]
    ecef2enu_rot = np.array([r1, r2, r3])

    # Calculate J2000 to body-equator-and-prime-meridian rotation matrix
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    j2000_to_earthfixed_rot = sp.tisbod(ref='J2000', body=399, et=et)[:3,:3]
    sp.kclear()

    # Calculate itrf, enu, altaz
    pos_itrf = np.matmul(j2000_to_earthfixed_rot, pos_gcrs)
    e, n, u = np.matmul(ecef2enu_rot, pos_itrf)
    r = np.hypot(e, n)
    rng = np.hypot(r, u)
    el = np.arctan2(u, r)
    az = np.mod(np.arctan2(e, n), 2*np.pi)    
    return az*r2d, el*r2d, rng


def get_crs(body, t, abcorr, obs, kernels):
    for k in kernels:
        sp.furnsh(k)
    et = sp.str2et(str(t))
    state, lt = sp.spkez(targ=body, et=et, ref='J2000', abcorr=abcorr, obs=obs)
    sp.kclear()
    pos = state[:3]
    vel = state[3:]
    return pos, vel, lt


def icrs(body, t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=body, t=t, abcorr=abccorr, obs=0, kernels=kernels)
    return pos


def gcrs(body, t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=body, t=t, abcorr=abccorr, obs=399, kernels=kernels)
    return pos


def earth_icrs(t, kernels, abccorr='NONE'):
    pos, _, _ = get_crs(body=399, t=t, abcorr=abccorr, obs=0, kernels=kernels)
    return pos

def icrs_to_gcrs(pos_icrs, t, kernels, abccorr='NONE'):
    earth = earth_icrs(t, kernels, abccorr)
    return pos_icrs - earth

def gcrs_to_icrs(pos_gcrs, t, kernels, abccorr='NONE'):
    earth = earth_icrs(t, kernels, abccorr)
    return pos_gcrs + earth

