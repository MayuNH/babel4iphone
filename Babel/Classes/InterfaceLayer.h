//
//  InterfaceLayer.h
//  Genoma
//
//  Created by Giovanni Amati on 24/11/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "cocos2d.h"

@interface InterfaceLayer : CCLayer
{
	int sel;        // indice dell'elemento selezionato del menu corrente
	int num;        // numero di item del menu corrente
	bool turn;
}

-(void) initMenu:(NSArray *)menuitems;   // inizializza il menu "name"
-(void) closeMenu;
-(void) configItem:(int)i move:(int)m;   // anima il menu in base a i e m
-(void) setTurn:(NSString *)name;        // imposta il turno

@end