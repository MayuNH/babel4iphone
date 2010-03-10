// This file is part of babel4iphone.

// Copyright (C) 2009 Giovanni Amati <amatig@gmail.com>

// babel4iphone is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// babel4iphone is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with babel4iphone.  If not, see <http://www.gnu.org/licenses/>.


#ifndef __INTERFACE_LAYER_H__
#define __INTERFACE_LAYER_H__

#define SHIFT 10000 // shifta i tag degli item dei menu da 10000 in poi
#define MOVE 20

#ifndef COCOS2D_VERSION
#import "cocos2d.h"
#endif

@interface InterfaceLayer : CCLayer
{
	int sel;        // indice dell'elemento selezionato del menu corrente
	int num;        // numero di item del menu corrente
	BOOL turn;
}

-(void) initMenu:(NSArray *)menuitems;   // inizializza il menu "name"
-(void) closeMenu;
-(void) configItem:(int)i move:(int)m;   // anima il menu in base a i e m
-(void) setTurn:(NSString *)name;        // imposta il turno

@end

#endif
