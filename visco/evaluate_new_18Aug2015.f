! Edit on 4th july 2019, by KVNG Vikram and P. Tregoning
! 'visco' option was giving zero output before.
! correction done by adding or 'visco' in if conditions along with 'vert' 
      program evaluate_sphharm

c  This is a program to evaluate a spherical harmonic representation of some field.
c  It can be used to tabulate the Stokes coefficient values across a particular
c  geographic region. The code is a cut-down version of grace_def.f in that it
c  doesn't make any attempt to convert the Stokes coefficients into any geophysically
c  meaningful values, and that it only outputs the values on a rectangular region
c  rather than the whole globe.
c
c  P. Tregoning
c  18 June 2007.

c   The Legendre polynomial code comes from Lambeck/Johnston/Zhang code that was part
c   of the calsea program.
c
c   P. Tregoning
c   14 March 2007
c
c PT100325: allow another command line argument, to specify the maximum degree to evaluate
c PT110713: allow stokes coefficients to be converted into either visco-elastic, elastic deformation, EWH or just as they are
c PT110802: if lat1 and lon1 = -99 then evaluate at a single point rather than on a grid
c PT111031: add to the program the computation of the formal error. It requires that the uncertainties are included in the input GRACE file(s). Formal errors are read in and stored in coef_errC and coef_errS
c AP111124: Added functionality to calculate lateral elastic deformation

      implicit none

      include 'grace_new.h'
      
      real*8 smooth_rad,love_ratio,lat,lon,colat,x,sumdef,rlat,rlong,sum
     .      ,cval,sval,minlat,minlon,maxlat,maxlon,stepsize,vfact,radius
     .      ,love_h(200),love_l(200),love_k(200),p_w,p_av,factor,factor_n
     .      ,sumvar,cerr,serr,vfact_up,vfact_tang,sumvar_up,sumdef_up
     .      ,sum_up,sumvar_east,sumvar_north,sum_east,sum_north
     .      ,sumdef_east,sumdef_north
      character arg*200,visco*5,line*100
      integer ideg,iord,i,j,l,m,ilat,ilon,isign,n,icomp,nm,ndeg,nord
     .       ,nstep(2),usedeg,itrash

c  define globally the value of pi (variable declared in grace.h)
      pi = 4.0d0*datan(1.d0) 
      radius = 6378100.d0
      earthrad = 6378100.00d0
      p_w = 1000.d0   ! kg/m^3 density of water
      p_av = 5515.d0  ! kg/m^3 average density of the Earth
      earthrad = 0.6378136460E+07 
      G = 6.67428e-11   ! gravitational constant (m**3/(kg s**2)
      mean_g = 9.81     ! mean gravity (m/s**2)
      factor = mean_g / (4.d0*pi*G*p_w*earthrad)     
c PT070523: in fact, since we are starting with Stokes coefficients we need
c           to multiply this by earthrad since Ramillien's equation assumes
c           that the coefficients are geoid coefficients (= Stokes * earthrad) 
c PT070523: while we're at it, change from m to mm
c PT110727: this is no longer used 
c      factor = earthrad*factor*1.d3

 
c  define the unit numbers for the i/o files
      lucoeff = 10
      lulove  = 20
      luout   = 30

c  open and read the file with the spherical harmonic coefficients
      call getarg(1,arg)
      if(arg(1:1).eq." ")then
        print*,"String: evaluate_sphharm <infile> <outfile> <min lat>"
     .         ,"<max lat> <min lon> <max lon> <stepsize> "
     .         ,  "<visco> <maxdeg>"
        print*,"e.g. evaluate_sphharm murray.hs junk -25. -15.  "
     .        ," 130. 135. 0.25 visco 50"
        print*,"To evaluate at only one point (rather than a grid)"
     . ,' use:    evaluate_sphharm gia_stokes.hs blah '
     . ,' 58.7590    -99      265.911     -99 10 visco '
        print*,'(ie replace maxlat and maxlon with -99) '
        stop
      endif

      open(lucoeff,file=arg,status='old',iostat=ioerr)
      if(ioerr.ne.0)then
        print*,'Error opening coefficients file: ',arg
        stop
      endif  

      call getarg(2,arg)
      open(luout,file=arg,status='unknown',iostat=ioerr)

      call getarg(3,arg)
      read(arg,*)minlat
      call getarg(4,arg)
      read(arg,*)maxlat

      call getarg(5,arg)
      read(arg,*)minlon
      call getarg(6,arg)
      read(arg,*)maxlon

      print*,minlat,maxlat,minlon,maxlon
      call getarg(7,arg)
      read(arg,*)stepsize

c PT080821: give this program the capability to convert to visco-elastic deformation
      call getarg(8,visco)

      call getarg(9,arg)
      if (arg(1:1).ne.' ')then
        read(arg,*)usedeg
      else
        usedeg = 0
      endif



      if(visco(1:5).eq.'visco')then
        print*,'will multiply by (1.1677n - 0.5233) to get mm vertical'

      elseif(visco(1:5).eq.'geoid')then
        print*,'will evaluate at the radius of the Earth'

      elseif((visco(1:5).eq.'edefn').or.(visco.eq.'vert')
     +     .or.(visco.eq.'north').or.(visco.eq.'east'))then
c  need the elastic love load numbers
        open(unit=11,file='Load_Love2_CM.dat'
     .                          ,status='old')
        do i=1,14
           read(11,'(a)')line
        enddo
        do i=1,200
           read(11,*)itrash,love_h(i),love_l(i),love_k(i)
        enddo
        print*,'will evaluate as elastic deformation'

      elseif(visco(1:3).eq.'ewh')then
c  need the elastic love load numbers
        open(unit=11,file='Load_Love2_CM.dat'
     .                       ,status='old')
        do i=1,14
           read(11,'(a)')line
        enddo
        do i=1,200
           read(11,*)itrash,love_h(i),love_l(i),love_k(i)
        enddo
        print*,'will determine equivalent water height of load'
      else
        print*,'will simply evaluate the field without changing units'
      endif





c the number of steps in latitude and longitude
      if (maxlat.ne.-99.d0.and.maxlon.ne.-99.d0)then
        nstep(1) = int( (maxlat - minlat)/stepsize)
        nstep(2) = int( (maxlon - minlon)/stepsize)
      else
        print*,'will evaluate only at location',minlat,minlon
        nstep(1) = 1
        nstep(2) = 1
c PT110802: if we set stepsize to zero then the code below will set the rlat/rlon coords to be minlat and minlon as we require !
        stepsize = 0
      endif


c  just read in the coefficients and store them away 
      ioerr = 0
      ndeg = 0
      do while (ioerr.eq.0)
        read(lucoeff,*,iostat=ioerr,end=1234)ideg,iord,cval,sval
     .          ,cerr,serr
        if(ioerr.eq.0)then 
          if(ideg.gt.ndeg)ndeg = ideg
          coefC(ideg+1,iord+1) = cval
          coefS(ideg+1,iord+1) = sval  
          coef_errC(ideg+1,iord+1) = cerr
          coef_errS(ideg+1,iord+1) = serr  
c      print*,ideg,iord,cval,sval,cerr,serr
        endif
      enddo

1234      print*,"Input sph harm model is up to degree ",ndeg

c PT100325: limit to maxdeg if it was input
      print*,'maxdeg and ndeg are',ndeg,usedeg

      if(usedeg.gt.0.and.usedeg.lt.ndeg) ndeg = usedeg
      print*,'will evaluate up to degree',ndeg

c   r(lambda, phi) = sum_l sum_m ( (  P_lm*(cos(th))
c                        *[ C_lm*cos(m*lambda) + S_lm*sin(m*lambda) ]

      do i = 1,nstep(1)
        rlat = minlat + (i-1)*stepsize 
        print*,'Latitude: ',rlat

c  compute the legendre polynomials for this spatial coordinate. They are
c  returned in Plm via the include file.
        rlat = rlat*pi/180.d0 
        colat = pi/2.d0-rlat 
        x = dcos(colat)
        call legendre(x,ndeg)

        do j = 1,nstep(2)
          rlong = minlon + (j-1)*stepsize  
c          print*,'longitude: ',rlong
          rlong = rlong*pi/180.d0
          sumdef = 0.d0
          sumdef_east = 0.d0
          sumdef_north = 0.d0
          sumdef_up = 0.d0
          sumvar = 0.d0
          sumvar_east = 0.d0
          sumvar_north = 0.d0
          sumvar_up = 0.d0
          sum = 0.d0 
          sum_up = 0.0d0
          sum_east = 0.0d0
          sum_north = 0.0d0

c  starting at degree/order of 2/0 means that the first legendre function required
c  is element 4
          nm = 4

          do  ideg = 2,  ndeg 

c PT080821: add a (2n+1)/2 factor - if required - to convert geoid to mm vertical deformation
            if(visco.eq.'visco')then
c PT110713: update this to use Amaury's regression values
c              vfact = earthrad*(2.d0*(ideg)+1.d0)/2.d0
              vfact = earthrad*(1.1677*ideg - 0.5233)*1000.d0
c                        convert to mm for visco-elastic deformation

            elseif(visco.eq.'geoid')then
              vfact = earthrad * 1000.d0  ! put it in mm

            elseif(visco(1:5).eq.'edefn')then
              vfact_up=earthrad*1.d3*love_h(ideg)/(1.d0+love_k(ideg))
              vfact_tang=earthrad*1.d3*love_l(ideg)/(1.d0+love_k(ideg))
c                        convert to mm for elastic deformation

            elseif(visco.eq.'north') then
               vfact = earthrad*1.d3*love_l(ideg)/(1.d0+love_k(ideg))
c                       convert to mm for elastic deformation

            elseif(visco.eq.'east') then
               vfact = earthrad*1.d3*love_l(ideg)/(1.d0+love_k(ideg))
c                      convert to mm for elastic deformation

            elseif(visco.eq.'vert') then
               vfact = earthrad*1.d3*love_h(ideg)/(1.d0+love_k(ideg))
c                     convert to mm for elastic deformation

            elseif(visco(1:3).eq.'ewh')then
               vfact = earthrad*p_av/(3.d0*p_w)*
     .                      (2.d0*ideg+1)/(1.d0+love_k(ideg))*1000.d0
c                    multiply here by 1000 to put it in mm
c               vfact=factor*((2.d0*float(ideg)+1)/(1.d0+love_k(ideg)))
            else
              vfact = 1.d0
            endif

c  compute the sectorial term (order = 0). Here, m=0, therefore the
c  C * cos(m*lambda) = C and the S coefficient is zero)
c  the multiplication by the cosine is multiplying only by 1.d0 so leave it off
            if ( visco.eq.'north') then
              sumdef = sumdef+vfact*dplm(nm)*coefC(ideg+1,1)  ! * cos(m*lambda)
              sumvar = sumvar+(vfact*dplm(nm)*coef_errC(ideg+1,1))**2
c again, leave out the  multiplication of dcos(iord*rlong) in the
c differentiation because it is 1.d0
            elseif ( visco .eq. 'east' ) then
              sumvar = sumvar+0.0d0
              sumdef = sumdef + 0.0d0
            elseif (visco.eq.'vert' .or. visco .eq. 'visco') then
              sumdef = sumdef+vfact*Plm(nm)*coefC(ideg+1,1)   ! * cos(m*lambda) 
              sumvar = sumvar+(vfact*plm(nm)*coef_errC(ideg+1,1))**2
            elseif (visco.eq.'ewh') then
              sumdef = sumdef+vfact*Plm(nm)*coefC(ideg+1,1)   ! * cos(m*lambda) 
              sumvar = sumvar+(vfact*plm(nm)*coef_errC(ideg+1,1))**2
            elseif ( visco .eq. 'edefn' ) then
              sumdef_north = sumdef_north
     +                  +vfact_tang*dplm(nm)*coefC(ideg+1,1)
              sumdef_east = sumdef_east + 0.0d0
              sumdef_up = sumdef_up+vfact_up*Plm(nm)*coefC(ideg+1,1)
              sumvar_north = sumvar_north
     +                  +(vfact_tang*dplm(nm)*coef_errC(ideg+1,1))**2
              sumvar_east = sumvar_east+0.0d0
              sumvar_up=sumvar_up
     +                  +(vfact_up*plm(nm)*coef_errC(ideg+1,1))**2
            endif
     
            nm = nm + 1
            do iord = 1, ideg   ! subtract 1 to correct for deg 0 offset in array 

c  the C and S coefficients are stored with (0 0) in array location (1 1) so we
c  need to correct for this offset. Here ideg has a value of 2 for degree 2 (so do  need
c  to add 1 to ideg) and iord has a value of 1 for order 0 and so also need to add one to get
c  the correct array element.
c
c PT070424: the normalisation used in calsea integrates to 2 whereas the
c           GRACE coefficients are normalised to 4 pi. To make the legendre
c           functions consistent with the GRACE coefficients we need to 
c           multiply the non-zonal legendre functions by sqrt(2)

c       print*,'Legendre for',ideg,iord,' : ',Plm(nm)*dsqrt(2.d0),vfact
              if (visco.eq.'north') then
                sum = vfact*dsqrt(2.0d0)*dplm(nm)
     +                *(coefC(ideg+1,iord+1)*dcos(iord*rlong) +
     +                  coefS(ideg+1,iord+1)*dsin(iord*rlong))   
                sumvar = sumvar 
     .             +2.d0*(vfact*dplm(nm))**2
     .             *((dcos(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dsin(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
              elseif (visco.eq.'east') then
                sum = vfact*dsqrt(2.0d0)*iord*(plm(nm)/dsin(colat))
     +                 *(coefS(ideg+1,iord+1)*dcos(iord*rlong) -
     +                   coefC(ideg+1,iord+1)*dsin(iord*rlong))
                sumvar = sumvar 
     .             +2.d0*(vfact*iord*(plm(nm)/dsin(colat)))**2
     .             *((dsin(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dcos(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
              elseif (visco.eq.'vert' .or. visco .eq. 'visco') then
                sum =  vfact*Plm(nm)*dsqrt(2.d0)                 
     .                *(coefC(ideg+1,iord+1)*dcos(iord*rlong)
     .                +coefS(ideg+1,iord+1)*dsin(iord*rlong) )
                sumvar = sumvar 
     .             +2.d0*(vfact*plm(nm))**2
     .             *((dcos(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dsin(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
              elseif (visco.eq.'ewh') then
                sum =  vfact*Plm(nm)*dsqrt(2.d0)                 
     .                *(coefC(ideg+1,iord+1)*dcos(iord*rlong)
     .                +coefS(ideg+1,iord+1)*dsin(iord*rlong) )
                sumvar = sumvar 
     .             +2.d0*(vfact*plm(nm))**2
     .             *((dcos(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dsin(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
              elseif (visco.eq.'edefn') then
                sum_up =  vfact_up*Plm(nm)*dsqrt(2.d0)                 
     .                *(coefC(ideg+1,iord+1)*dcos(iord*rlong)
     .                +coefS(ideg+1,iord+1)*dsin(iord*rlong) )
                sumvar_up = sumvar_up 
     .             +2.d0*(vfact_up*plm(nm))**2
     .             *((dcos(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dsin(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
          sum_east = vfact_tang*dsqrt(2.0d0)*iord*(plm(nm)/dsin(colat))
     +                 *(coefS(ideg+1,iord+1)*dcos(iord*rlong) -
     +                   coefC(ideg+1,iord+1)*dsin(iord*rlong))
                sumvar_east = sumvar_east
     .             +2.d0*(vfact_tang*iord*(plm(nm)/dsin(colat)))**2
     .             *((dsin(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dcos(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
                sum_north = vfact_tang*dsqrt(2.0d0)*dplm(nm)
     +                *(coefC(ideg+1,iord+1)*dcos(iord*rlong) +
     +                  coefS(ideg+1,iord+1)*dsin(iord*rlong))   
                sumvar_north = sumvar_north 
     .             +2.d0*(vfact_tang*dplm(nm))**2
     .             *((dcos(iord*rlong)*coef_errC(ideg+1,iord+1))**2
     .              +(dsin(iord*rlong)*coef_errS(ideg+1,iord+1))**2)
              endif



c               write(*,'(2i5,4e20.12)')ideg,iord,Plm(nm)
c     .              ,coefC(ideg+1,iord+1),coefS(ideg+1,iord+1)
c     .               , Plm(nm)*dsqrt(2.d0)                 
c     .             *(coefC(ideg+1,iord+1)*dcos(iord*rlong)
c     .             +coefS(ideg+1,iord+1)*dsin(iord*rlong) )
              if (visco.ne.'edefn') then
                sumdef = sumdef + sum
              else
                sumdef_up = sumdef_up + sum_up
                sumdef_east = sumdef_east + sum_east
                sumdef_north = sumdef_north + sum_north
              endif
              nm = nm + 1
            enddo
          enddo
c  PT070402: for some reason it seems to be the negative of what I expected.
c            At the same time, scale it to mm and set long range to -180/180
          if (rlong.gt.pi)rlong = rlong-2.d0*pi
          if ( visco.eq.'north' ) sumdef = -sumdef
          if ( visco.eq.'edefn' ) then
            sumdef_north = -sumdef_north
          write(luout,'(2f10.2,3f9.3,3f8.3)')rlat*180.d0/pi
     .         ,rlong*180.d0/pi,sumdef_north,sumdef_east,sumdef_up
     .         ,dsqrt(sumvar_north),dsqrt(sumvar_east),dsqrt(sumvar_up)
          else
            write(luout,'(2f10.2,2f30.14)')rlat*180.d0/pi
     .         ,rlong*180.d0/pi,1.d0*sumdef,dsqrt(sumvar)
          endif
        enddo
      enddo

      end


      subroutine legendre(X,ndeg)
c
c     calculate the normalised associated Legendre function values at x up to degree ndeg
c
c     The normalisation is such that the integral of Pnm^2 from -1 to 1 is 2.
c     This is slightly different from the normalisation used in the older
c     sea-level programs.  In those programs, if m is not equal to 0, the
c     normalisation had an extra factor sqrt(2), so that integral over the
c     sphere of Pnm cos or sin m phi is 4 pi.  With this normalisation
c     the integral over the sphere of Pnm exp(i m phi) is equal to 4 pi.
c
c PT070326: compute only to the maximum degree of the input file, ndeg, rather
c           than to the maximum dimensioned degree.
c
c PT070402: this subroutine assumes that the array of Legendre functions
c           goes from P(0) to P(ndeg). Didn't know that you could start at zero! 
c           You can't! I had to change it to go from 1 to ndeg+1
     
      implicit none

      include 'grace_new.h'

c input co-latitude in radians
      real*8 X

c local variables
      real*8 aa,as,s,sum,c,d,c0
      integer i,j,l,m,l0,i0,i1,i2,ndeg


      aa=1.0d0-x*x
      as=dsqrt(aa)
      Plm(1)=1
      Plm(2)=X
      dplm(1)=0.0d0
      dplm(2)=-as
      i1=1
      i2=2
      do i=2,ndeg
        i0=i1
        i1=i2
        i2=i*(i+1)/2+1
        Plm(i2)=((2*i-1)*X*Plm(i1)-(i-1)*Plm(i0))/i 
        dplm(i2)=((2.d0*i-1.d0)*(-as*plm(i1)+x*dplm(i1))
     +                -(i-1.d0)*dplm(i0))/float(i)
         if(i2.eq.2)print*,'Plm(2)',Plm(2)
c        print*,'legendre: ',i,i2,Plm(i2),earthrad
      enddo

      do i=1,ndeg
        i2=i*(i+1)/2+1
        Plm(i2)=dsqrt(2.d0*i+1)*Plm(i2)
        dplm(i2)=dsqrt(2.d0*i+1)*dplm(i2)
c         if(i2.eq.2)print*,'2 Plm(2)',Plm(2)
c        print*,'legendre 2: ',i,i2,Plm(i2),earthrad
      enddo

      AA=1.d0-X*X
      IF(AA.eq.0) then
        DO 200 l=0,ndeg
         l0=l*(l+1)/2+1
         do 200 m=1,l
c         if(m.eq.2)print*,'Plm(2)',Plm(2)
200       Plm(m+l0)=0
        RETURN    
      endif

c      print*,'still in legendre'
      AS=dSQRT(AA)
      Plm(3)=AS*dSQRT(1.5D0)
      Plm(5)=3*AS*X*dSQRT(2.5D0/3.d0)
      Plm(6)=3*AA*dSQRT(5.D0/24.d0)
      dplm(3)=x*sqrt(1.5d0)
      dplm(5)=3.0d0*dSQRT(2.5D0/3.d0)*(aa-x*x)/as
      dplm(6)=-6.0d0*x*dSQRT(5.D0/24.d0)

      DO l=3,ndeg
        SUM=1.d0
        DO  J=1,l
          S=float(2*J-1)/(2.d0*J)
          SUM=SUM*dSQRT(AA*S) 
        enddo
        l0=l*(l+1)/2+1
        Plm(l+l0)=SUM*dSQRT(2.D0*l+1.d0)
        dplm(l+l0)=dfloat(l-1)*x/as*plm(l+l0)
c         if(l+l0.eq.2)print*,'3 Plm(2)',Plm(2)
c        print*,'legendre 3: ',l,l+l0,Plm(l+l0),earthrad
        SUM=1.d0
        DO  J=2,l
          S=float(2*J-1)/(2*J-2.d0)
          SUM=SUM*dSQRT(AA*S)
        enddo
        plm(l-1+l0)=X*dSQRT(2.D0*l+1.d0)*SUM
        dplm(l-1+l0)=-as*SQRT(dfloat(2*l+1))*SUM
     +                   +dfloat(l-1)*x/as*plm(l-1+l0)
c         if(l-1+l0.eq.2)print*,'Plm(2)',Plm(2)
c        print*,'legendre 4: ',l,Plm(l-1+l0),earthrad
        DO  M=l-2,1,-1
          C0=2.d0*(M+1)/dSQRT((l+M+1.D0)*(l-M))
          C=C0*X/AS
          D=(l+M+2)*(l-M-1)/((l+M+1.D0)*(l-M))
          D=dSQRT(D)
          Plm(M+l0)=C*Plm(M+1+l0)-D*Plm(M+2+l0)  
          dplm(m+l0)=-c0/aa*plm(m+1+l0)+c*dplm(m+1+l0)-d*dplm(m+2+l0)
         if(M+l0.eq.2)print*,'Plm(2)',Plm(2)
c        print*,'legendre 5: ',l,m,m+l0,Plm(m+l0),earthrad
c        if(m.eq.19.and.l.eq.34)then
c          print*,C,Plm(M+1+l0),D,Plm(M+2+l0),l0
c          stop
c        endif
        enddo
      enddo

c      print*,'end of legendre Plm(2)',Plm(2)
      end


